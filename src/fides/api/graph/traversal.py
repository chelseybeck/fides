from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Set, Tuple, cast

import pydash.collections
from fideslang.validation import FidesKey
from loguru import logger

from fides.api.common_exceptions import TraversalError
from fides.api.graph.config import (
    ROOT_COLLECTION_ADDRESS,
    TERMINATOR_ADDRESS,
    Collection,
    CollectionAddress,
    FieldAddress,
    FieldPath,
    GraphDataset,
)
from fides.api.graph.execution import ExecutionNode
from fides.api.graph.graph import DatasetGraph, Edge, Node
from fides.api.models.privacy_request import RequestTask, TraversalDetails
from fides.api.util.collection_util import Row, append, partition
from fides.api.util.logger_context_utils import Contextualizable, LoggerContextKeys
from fides.api.util.matching_queue import MatchingQueue

ARTIFICIAL_NODES: List[CollectionAddress] = [
    ROOT_COLLECTION_ADDRESS,
    TERMINATOR_ADDRESS,
]

Datastore = Dict[CollectionAddress, List[Row]]
"""A type expressing retrieved rows of data from a specified collection"""


class TraversalNode(Contextualizable):
    """Traversal_node type. This type is used for building the graph, not for executing the graph."""

    def __init__(self, node: Node):
        self.node = node
        self.address = node.address
        # address to a child that holds both a traversal_node and all possible paths
        # from this traversal_node to it: {address -> [(traversal_node, from_field, to_field)}
        self.children: Dict[
            CollectionAddress, List[Tuple[TraversalNode, FieldPath, FieldPath]]
        ] = {}
        self.parents: Dict[
            CollectionAddress, List[Tuple[TraversalNode, FieldPath, FieldPath]]
        ] = {}
        self.is_terminal_node = False

    def add_child(self, child_node: TraversalNode, edge: Edge) -> None:
        """Add other as a child to this traversal_node along the provided edge."""
        addresses = edge.split_by_address(self.address)  # (traversal_node -> other)
        if addresses:
            self_field_address, other_field_address = addresses
            append(
                self.children,
                other_field_address.collection_address(),
                (
                    child_node,
                    self_field_address.field_path,
                    other_field_address.field_path,
                ),
            )
            append(
                child_node.parents,
                self_field_address.collection_address(),
                (self, self_field_address.field_path, other_field_address.field_path),
            )

    def incoming_edges(self) -> Set[Edge]:
        """Return the incoming edges to this traversal_node,in (other.address -> self.address) order."""
        return {
            Edge(
                p_collection_address.field_address(parent_field_path),
                self.address.field_address(self_field_path),
            )
            for p_collection_address, tuples in self.parents.items()
            for _, parent_field_path, self_field_path in tuples
        }

    def outgoing_edges(self) -> Set[Edge]:
        """Return the outgoing edges to this traversal_node,in (self.address -> other.address) order."""
        return {
            Edge(
                self.address.field_address(self_field_path),
                c_collection_address.field_address(child_field_path),
            )
            for c_collection_address, tuples in self.children.items()
            for _, self_field_path, child_field_path in tuples
        }

    def incoming_edges_by_collection(self) -> Dict[CollectionAddress, List[Edge]]:
        return partition(self.incoming_edges(), lambda e: e.f1.collection_address())

    def input_keys(self) -> List[CollectionAddress]:
        """Returns the inputs to the current node that are data dependencies
        This is copied and saved to the RequestTask and used to maintain a consistent order
        for passing in data for an access task
        """
        return sorted(self.incoming_edges_by_collection().keys())

    def can_run_given(self, remaining_node_keys: Set[CollectionAddress]) -> bool:
        """True if finished_node_keys covers all the nodes that this traversal_node is waiting for.  If
        all nodes this traversal_node is waiting for have finished, it's ok for this traversal_node to run.

        NOTE: "After" functionality may not work as expected.
        """
        if self.node.collection.after.intersection(
            remaining_node_keys
        ) or self.node.dataset.after.intersection(
            {k.dataset for k in remaining_node_keys}
        ):
            return False
        return True

    def is_root_node(self) -> bool:
        """This traversal_node is the defined traversal start"""
        return self.address == ROOT_COLLECTION_ADDRESS

    def debug(self) -> Dict[str, Any]:
        """Generate debug descriptive output of the traversal."""
        _from: Dict[str, Set[str]] = {}

        for edge in self.incoming_edges():
            foreign = edge.f1
            local = edge.f2
            # if we have a bidirectional edge, make sure that we correctly label
            # which edge is foreign.
            if foreign.collection_address() == self.address:
                foreign, local = local, foreign
            key = str(foreign.collection_address())
            val = f"{foreign.field_path.string_path} -> {local.field_path.string_path}"
            if key in _from:
                _from[key].add(val)
            else:
                _from[key] = {val}
        to: Dict[str, Set[str]] = {}
        for k, v in self.children.items():
            to[str(k)] = {f"{f[1].string_path} -> {f[2].string_path}" for f in v}
        return {
            "from": {k: set(v) for k, v in _from.items()},
            "to": {k: set(v) for k, v in to.items()},
        }

    def get_log_context(self) -> Dict[LoggerContextKeys, Any]:
        return {LoggerContextKeys.collection: self.node.collection.name}

    def format_traversal_details_for_save(self) -> Dict:
        """Convert key traversal details from the TraversalNode for save on the RequestTask.

        The RequestTask will be retrieved from the database and the traversal details
        used to build the ExecutionNode for DSR 3.0.
        """

        connection_key: FidesKey = self.node.dataset.connection_key

        return TraversalDetails(
            dataset_connection_key=connection_key,
            incoming_edges=[
                [edge.f1.value, edge.f2.value] for edge in self.incoming_edges()
            ],
            outgoing_edges=[
                [edge.f1.value, edge.f2.value] for edge in self.outgoing_edges()
            ],
            input_keys=[tn.value for tn in self.input_keys()],
        ).model_dump(mode="json")

    def to_mock_request_task(self) -> RequestTask:
        """Converts a portion of the TraversalNode into a RequestTask - used in building
        dry run queries or for supporting Deprecated DSR 2.0. Request Tasks were introduced in DSR 3.0
        """
        collection_data = json.loads(
            # Serializes with duck-typing behavior, no longer the default in Pydantic v2
            # Needed for serializing nested collection fields
            self.node.collection.model_dump_json(serialize_as_any=True)
        )
        return RequestTask(  # Mock a RequestTask object in memory
            collection_address=self.node.address.value,
            dataset_name=self.node.address.dataset,
            collection_name=self.node.address.collection,
            collection=collection_data,
            traversal_details=self.format_traversal_details_for_save(),
        )

    def to_mock_execution_node(self) -> ExecutionNode:
        """Converts a TraversalNode into an ExecutionNode - used for supporting DSR 2.0, to convert
        Traversal Nodes into the Execution Node format which is needed for executing the graph in
        DSR 3.0

        DSR 3.0 on the other hand, creates ExecutionNodes from data on the RequestTask.
        """
        request_task: RequestTask = self.to_mock_request_task()
        return ExecutionNode(request_task)


def artificial_traversal_node(address: CollectionAddress) -> TraversalNode:
    """generate an 'artificial' traversal_node pointing to the given address. This is used to
    generate artificial root and termination nodes that correspond to just an address, but
    have no actual corresponding collection dataset"""
    ds: Collection = Collection(name=address.collection, fields=[])
    node = Node(
        GraphDataset(
            name=address.dataset, collections=[ds], connection_key="__IGNORE__"
        ),
        ds,
    )
    return TraversalNode(node)


class Traversal:
    """Handling for a single reified traversal of a graph based on input (seed) data."""

    def extract_seed_field_addresses(
        self,
    ) -> Dict[FieldAddress, str]:
        """Find seeded values in the graph based on the input seed and return
        a list of the populated seed nodes"""

        return {
            identity_address: seed_key
            for identity_address, seed_key in self.graph.identity_keys.items()
            if seed_key in self.seed_data
        }

    def __init__(self, graph: DatasetGraph, data: Dict[str, Any]):
        self.graph = graph
        self.seed_data = data
        self.traversal_node_dict = {k: TraversalNode(v) for k, v in graph.nodes.items()}
        self.edges: Set[Edge] = graph.edges.copy()
        self.root_node = artificial_traversal_node(ROOT_COLLECTION_ADDRESS)
        for (
            start_field_address,
            seed_key,
        ) in self.extract_seed_field_addresses().items():
            self.edges.add(
                Edge(
                    FieldAddress(
                        ROOT_COLLECTION_ADDRESS.dataset,
                        ROOT_COLLECTION_ADDRESS.collection,
                        seed_key,
                    ),
                    start_field_address,
                )
            )

        self.__verify_traversal()

    def __verify_traversal(self) -> None:
        """Verify that a valid traversal exists. This method simply assembles a traversal
        and raises an error on any traversal failure conditions."""
        self.traverse(
            {self.root_node.address: [self.seed_data]},
            lambda n, m: logger.info("Traverse {}", n.address),
        )

    def traversal_map(
        self,
    ) -> Tuple[Dict[str, List[Dict[str, Any]]], List[CollectionAddress]]:
        """Generate a descriptive map of the traversal generated.

        For each traversal_node N, list
         { N.address:
             {"from": {traversal_node address:
                       [field in "from", field in N for all edges from "from" to N]}}
             {"to": {traversal_node address,
                       [field in N, field in "to"" for all edges from N to "to"]}}

        """

        def traversal_dict_fn(
            tn: TraversalNode, data: Dict[CollectionAddress, Dict[str, Any]]
        ) -> None:
            data[tn.address] = tn.debug()

        db = {ROOT_COLLECTION_ADDRESS: [self.seed_data]}
        traversal_ends = self.traverse(db, traversal_dict_fn)

        return {str(k): v for k, v in db.items()}, traversal_ends

    def traverse(  # pylint: disable=R0914
        self,
        environment: Dict[CollectionAddress, Any],
        node_run_fn: Callable[[TraversalNode, Dict[CollectionAddress, Any]], None],
    ) -> List[CollectionAddress]:
        """Traverse and call run() on each traversal_node in turn. T represents an environment that
        can provide or collect values as each traversal_node is run.

        Returns a list of termination traversal_node addresses so that we can take action on completed
        traversal.

        We define the root traversal_node as a traversal_node whose children are any nodes that have identity (seed)
        data.
        We start with
        - a queue holding only the root traversal_node.
        - a (copied) set of all of the edges in the graph.

        - Pop the first eligible traversal_node from the queue.
        - call the passed in callable node_run_function on this traversal_node. Mark this traversal_node as "finished"
        - Delete all edges from any finished nodes to this traversal_node.
        - put all of this nodes children in the queue.

        Some nodes have conditions, like "don't run me until after traversal_node X". When we pop a value from
        the queue, we are taking this into account. If the queue contains nodes, but none of them are
        eligible (e.g. Node A can't run until after B, and traversal_node B that can't run until after A)
        raise a TraversalError.

        We also raise a TraversalError if the queue is empty but some nodes have not been visited. In
        that case they are unreachable.

        """
        if environment:
            logger.info(
                "starting traversal",
            )
        remaining_node_keys: Set[CollectionAddress] = set(
            self.traversal_node_dict.keys()
        )
        finished_nodes: dict[CollectionAddress, TraversalNode] = {}
        running_node_queue: MatchingQueue[TraversalNode] = MatchingQueue(self.root_node)
        remaining_edges: Set[Edge] = self.edges.copy()
        while not running_node_queue.is_empty():
            # this is to support the "run traversal_node A AFTER traversal_node B functionality:"
            n = running_node_queue.pop_first_match(
                lambda x: x.can_run_given(remaining_node_keys)
            )

            if n:
                node_run_fn(n, environment)
                # delete all edges between the traversal_node that's just run and any completed nodes
                for finished_node_address, finished_node in finished_nodes.items():
                    completed_edges: Set[Edge] = Edge.delete_edges(
                        remaining_edges,
                        finished_node_address,
                        cast(TraversalNode, n).address,  # type: ignore[redundant-cast]
                    )

                    def edge_ends_with_collection(_edge: Edge) -> bool:
                        # append edges that end in this traversal_node
                        return _edge.ends_with_collection(
                            cast(TraversalNode, n).address  # type: ignore[redundant-cast]
                        )

                    for edge in filter(edge_ends_with_collection, completed_edges):
                        # note, this will not work for self-reference
                        finished_node.add_child(n, edge)
                # next edges = take all edges including n that are _not_ in edges_from_completed_nodes
                # in the form (field_address_this, field_address_foreign)

                edges_to_children = pydash.collections.filter_(
                    [
                        e.split_by_address(cast(TraversalNode, n).address)  # type: ignore[redundant-cast]
                        for e in remaining_edges
                        if e.contains(n.address)
                    ]
                )
                if not edges_to_children:
                    n.is_terminal_node = True

                # child traversal_node addresses are the address portion of the above
                child_node_addresses = {
                    a[1].collection_address() for a in edges_to_children if a
                }
                for nxt_address in child_node_addresses:
                    # only add the next traversal_node to the queue if it is not already there (no duplicates)
                    running_node_queue.push_if_new(
                        self.traversal_node_dict[nxt_address]
                    )
                finished_nodes[n.address] = n
                remaining_node_keys.difference_update({n.address})
            else:
                # traversal traversal_node dict diff finished nodes
                logger.error(
                    "Node could not be reached given specified ordering [{}]",
                    ",".join([str(tn.address) for tn in running_node_queue.data]),
                )
                raise TraversalError(
                    f"""Node could not be reached given the specified ordering:
                    [{','.join([str(tn.address) for tn in running_node_queue.data])}]"""
                )

        # Remove nodes that have custom request fields, since we don't care if these are reachable or not.
        # They will be used independently by the Dynamic Email Erasure Connector.
        # TODO: ideally we'll update the Traversal code to include these "custom request field datasets"
        # as part of the main graph. This is a targeted workaround for now.
        remaining_node_keys = set(
            key
            for key in remaining_node_keys
            if not self.traversal_node_dict[key].node.collection.custom_request_fields()
        )

        # error if there are nodes that have not been visited
        if remaining_node_keys:
            logger.error(
                "Some nodes were not reachable: {}",
                ",".join([str(x) for x in remaining_node_keys]),
            )
            raise TraversalError(
                f"Some nodes were not reachable: {','.join([str(x) for x in remaining_node_keys])}"
            )

        # error if there are edges that have not been visited
        if remaining_edges:
            logger.error(
                "Some edges were not reachable: {}",
                ",".join([str(x) for x in remaining_edges]),
            )
            raise TraversalError(
                f"Some edges were not reachable: {','.join([str(x) for x in remaining_edges])}"
            )

        end_nodes = [
            tn.address for tn in finished_nodes.values() if tn.is_terminal_node
        ]
        if environment:
            logger.debug("Found {} end nodes: {}", len(end_nodes), end_nodes)
        return end_nodes
