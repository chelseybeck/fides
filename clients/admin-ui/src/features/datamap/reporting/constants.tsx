/* eslint-disable @typescript-eslint/naming-convention */

export enum DATAMAP_LOCAL_STORAGE_KEYS {
  COLUMN_EXPANSION_STATE = "datamap-column-expansion-state",
  COLUMN_NAMES = "datamap-column-names",
  COLUMN_ORDER = "datamap-column-order",
  COLUMN_SIZING = "datamap-column-sizing",
  COLUMN_VISIBILITY = "datamap-column-visibility",
  CUSTOM_REPORT_ID = "datamap-custom-report-id",
  FILTERS = "datamap-filters",
  GROUP_BY = "datamap-group-by",
  SORTING_STATE = "datamap-sorting-state",
  WRAPPING_COLUMNS = "datamap-wrapping-columns",
}

export enum COLUMN_IDS {
  SYSTEM_NAME = "system_name",
  DATA_USE = "data_use",
  DATA_CATEGORY = "data_categories",
  DATA_SUBJECT = "data_subjects",
  LEGAL_NAME = "legal_name",
  DPO = "dpo",
  LEGAL_BASIS_FOR_PROCESSING = "legal_basis_for_processing",
  ADMINISTRATING_DEPARTMENT = "administrating_department",
  COOKIE_MAX_AGE_SECONDS = "cookie_max_age_seconds",
  PRIVACY_POLICY = "privacy_policy",
  LEGAL_ADDRESS = "legal_address",
  COOKIE_REFRESH = "cookie_refresh",
  DATA_SECURITY_PRACTICES = "data_security_practices",
  DATA_SHARED_WITH_THIRD_PARTIES = "DATA_SHARED_WITH_THIRD_PARTIES",
  DATA_STEWARDS = "data_stewards",
  DECLARATION_NAME = "declaration_name",
  DOES_INTERNATIONAL_TRANSFERS = "does_international_transfers",
  DPA_LOCATION = "dpa_location",
  DESTINATIONS = "egress",
  EXEMPT_FROM_PRIVACY_REGULATIONS = "exempt_from_privacy_regulations",
  FEATURES = "features",
  FIDES_KEY = "fides_key",
  FLEXIBLE_LEGAL_BASIS_FOR_PROCESSING = "flexible_legal_basis_for_processing",
  IMPACT_ASSESSMENT_LOCATION = "impact_assessment_location",
  SOURCES = "ingress",
  JOINT_CONTROLLER_INFO = "joint_controller_info",
  LEGAL_BASIS_FOR_PROFILING = "legal_basis_for_profiling",
  LEGAL_BASIS_FOR_TRANSFERS = "legal_basis_for_transfers",
  LEGITIMATE_INTEREST_DISCLOSURE_URL = "legitimate_interest_disclosure_url",
  LINK_TO_PROCESSOR_CONTRACT = "link_to_processor_contract",
  PROCESSES_PERSONAL_DATA = "processes_personal_data",
  REASON_FOR_EXEMPTION = "reason_for_exemption",
  REQUIRES_DATA_PROTECTION_ASSESSMENTS = "requires_data_protection_assessments",
  RESPONSIBILITY = "responsibility",
  RETENTION_PERIOD = "retention_period",
  SHARED_CATEGORIES = "shared_categories",
  SPECIAL_CATEGORY_LEGAL_BASIS = "special_category_legal_basis",
  SYSTEM_DEPENDENCIES = "system_dependencies",
  THIRD_COUNTRY_SAFEGUARDS = "third_country_safeguards",
  THIRD_PARTIES = "third_parties",
  COOKIES = "cookies",
  USES_COOKIES = "uses_cookies",
  USES_NON_COOKIE_ACCESS = "uses_non_cookie_access",
  USES_PROFILING = "uses_profiling",
  SYSTEM_UNDECLARED_DATA_CATEGORIES = "system_undeclared_data_categories",
  DATA_USE_UNDECLARED_DATA_CATEGORIES = "data_use_undeclared_data_categories",
}

export const DEFAULT_COLUMN_NAMES: Record<COLUMN_IDS, string> = {
  [COLUMN_IDS.SYSTEM_NAME]: "System",
  [COLUMN_IDS.DATA_USE]: "Data use",
  [COLUMN_IDS.DATA_CATEGORY]: "Data categories",
  [COLUMN_IDS.DATA_SUBJECT]: "Data subject",
  [COLUMN_IDS.LEGAL_NAME]: "Legal name",
  [COLUMN_IDS.DPO]: "Data privacy officer",
  [COLUMN_IDS.LEGAL_BASIS_FOR_PROCESSING]: "Legal basis for processing",
  [COLUMN_IDS.ADMINISTRATING_DEPARTMENT]: "Administrating department",
  [COLUMN_IDS.COOKIE_MAX_AGE_SECONDS]: "Cookie max age seconds",
  [COLUMN_IDS.PRIVACY_POLICY]: "Privacy policy",
  [COLUMN_IDS.LEGAL_ADDRESS]: "Legal address",
  [COLUMN_IDS.COOKIE_REFRESH]: "Cookie refresh",
  [COLUMN_IDS.DATA_SECURITY_PRACTICES]: "Data security practices",
  [COLUMN_IDS.DATA_SHARED_WITH_THIRD_PARTIES]: "Data shared with third parties",
  [COLUMN_IDS.DATA_STEWARDS]: "Data stewards",
  [COLUMN_IDS.DECLARATION_NAME]: "Declaration name",
  [COLUMN_IDS.DOES_INTERNATIONAL_TRANSFERS]: "Does international transfers",
  [COLUMN_IDS.DPA_LOCATION]: "DPA location",
  [COLUMN_IDS.DESTINATIONS]: "Destinations",
  [COLUMN_IDS.EXEMPT_FROM_PRIVACY_REGULATIONS]:
    "Exempt from privacy regulations",
  [COLUMN_IDS.FEATURES]: "Features",
  [COLUMN_IDS.FIDES_KEY]: "Fides key",
  [COLUMN_IDS.FLEXIBLE_LEGAL_BASIS_FOR_PROCESSING]:
    "Flexible legal basis for processing",
  [COLUMN_IDS.IMPACT_ASSESSMENT_LOCATION]: "Impact assessment location",
  [COLUMN_IDS.SOURCES]: "Sources",
  [COLUMN_IDS.JOINT_CONTROLLER_INFO]: "Joint controller info",
  [COLUMN_IDS.LEGAL_BASIS_FOR_PROFILING]: "Legal basis for profiling",
  [COLUMN_IDS.LEGAL_BASIS_FOR_TRANSFERS]: "Legal basis for transfers",
  [COLUMN_IDS.LEGITIMATE_INTEREST_DISCLOSURE_URL]:
    "Legitimate interest disclosure URL",
  [COLUMN_IDS.LINK_TO_PROCESSOR_CONTRACT]: "Link to processor contract",
  [COLUMN_IDS.PROCESSES_PERSONAL_DATA]: "Processes personal data",
  [COLUMN_IDS.REASON_FOR_EXEMPTION]: "Reason for exemption",
  [COLUMN_IDS.REQUIRES_DATA_PROTECTION_ASSESSMENTS]:
    "Requires data protection assessments",
  [COLUMN_IDS.RESPONSIBILITY]: "Responsibility",
  [COLUMN_IDS.RETENTION_PERIOD]: "Retention period",
  [COLUMN_IDS.SHARED_CATEGORIES]: "Shared categories",
  [COLUMN_IDS.SPECIAL_CATEGORY_LEGAL_BASIS]: "Special category legal basis",
  [COLUMN_IDS.SYSTEM_DEPENDENCIES]: "System dependencies",
  [COLUMN_IDS.THIRD_COUNTRY_SAFEGUARDS]: "Third country safeguards",
  [COLUMN_IDS.THIRD_PARTIES]: "Third parties",
  [COLUMN_IDS.SYSTEM_UNDECLARED_DATA_CATEGORIES]:
    "System undeclared data categories",
  [COLUMN_IDS.DATA_USE_UNDECLARED_DATA_CATEGORIES]:
    "Data use undeclared data categories",
  [COLUMN_IDS.COOKIES]: "Cookies",
  [COLUMN_IDS.USES_COOKIES]: "Uses cookies",
  [COLUMN_IDS.USES_NON_COOKIE_ACCESS]: "Uses non-cookie access",
  [COLUMN_IDS.USES_PROFILING]: "Uses profiling",
};