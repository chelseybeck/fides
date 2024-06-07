import {
  Box,
  Button,
  ButtonGroup,
  Flex,
  Spacer,
  Spinner,
  useDisclosure,
} from "fidesui";
import { NextPage } from "next";
import { useRouter } from "next/router";

import DataTabs, { TabData } from "~/features/common/DataTabs";
import Layout from "~/features/common/Layout";
import { INTEGRATION_MANAGEMENT_ROUTE } from "~/features/common/nav/v2/routes";
import PageHeader from "~/features/common/PageHeader";
import { useGetDatastoreConnectionByKeyQuery } from "~/features/datastore-connections";
import useTestConnection from "~/features/datastore-connections/useTestConnection";
import BigQueryOverview, {
  BigQueryInstructions,
} from "~/features/integrations/bigqueryOverviewCopy";
import MonitorConfigTab from "~/features/integrations/configure-monitor/MonitorConfigTab";
import ConfigureIntegrationModal from "~/features/integrations/ConfigureIntegrationModal";
import ConnectionStatusNotice from "~/features/integrations/ConnectionStatusNotice";
import IntegrationBox from "~/features/integrations/IntegrationBox";

const IntegrationDetailView: NextPage = () => {
  const { query } = useRouter();
  const id = Array.isArray(query.id) ? query.id[0] : query.id;
  const { data: connection, isLoading: integrationIsLoading } =
    useGetDatastoreConnectionByKeyQuery(id ?? "");

  const {
    testConnection,
    isLoading: testIsLoading,
    testData,
  } = useTestConnection(connection);

  const { onOpen, isOpen, onClose } = useDisclosure();
  const tabs: TabData[] = [
    {
      label: "Connection",
      content: (
        <Box maxW="720px">
          <Flex
            borderRadius="md"
            outline="1px solid"
            outlineColor="gray.100"
            align="center"
            p={3}
          >
            <Flex flexDirection="column">
              <ConnectionStatusNotice testData={testData} />
            </Flex>
            <Spacer />
            <ButtonGroup size="sm" variant="outline">
              <Button
                onClick={testConnection}
                isLoading={testIsLoading}
                data-testid="test-connection-btn"
              >
                Test connection
              </Button>
              <Button onClick={onOpen} data-testid="manage-btn">
                Manage
              </Button>
            </ButtonGroup>
          </Flex>
          <ConfigureIntegrationModal
            isOpen={isOpen}
            onClose={onClose}
            connection={connection!}
          />
          <BigQueryOverview />
          <BigQueryInstructions />
        </Box>
      ),
    },
    {
      label: "Data discovery",
      content: <MonitorConfigTab integration={connection!} />,
    },
  ];

  return (
    <Layout title="Integrations">
      <PageHeader
        breadcrumbs={[
          {
            title: "Integrations",
            link: INTEGRATION_MANAGEMENT_ROUTE,
          },
          {
            title: connection?.name ?? connection?.key ?? "",
          },
        ]}
      >
        <IntegrationBox integration={connection} />
        {integrationIsLoading ? <Spinner /> : <DataTabs data={tabs} isLazy />}
      </PageHeader>
    </Layout>
  );
};

export default IntegrationDetailView;
