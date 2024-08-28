import { h, VNode } from "preact";

import {
  ConsentMethod,
  FidesInitOptions,
  PrivacyExperience,
  PrivacyExperienceMinimal,
} from "../../lib/consent-types";
import type { EnabledIds, TcfModels } from "../../lib/tcf/types";
import { ConsentButtons } from "../ConsentButtons";

interface TcfConsentButtonProps {
  experience: PrivacyExperience | PrivacyExperienceMinimal;
  options: FidesInitOptions;
  onManagePreferencesClick?: () => void;
  onSave: (consentMethod: ConsentMethod, keys: EnabledIds) => void;
  renderFirstButton?: () => VNode;
  isInModal?: boolean;
}

const getAllIds = (modelList: TcfModels) => {
  if (!modelList) {
    return [];
  }
  return modelList.map((m) => `${m.id}`);
};

export const TcfConsentButtons = ({
  experience,
  onManagePreferencesClick,
  onSave,
  renderFirstButton,
  isInModal,
  options,
}: TcfConsentButtonProps) => {
  if (!experience.experience_config) {
    return null;
  }

  const handleAcceptAll = () => {
    if (!experience.minimal_tcf) {
      // eslint-disable-next-line no-param-reassign
      experience = experience as PrivacyExperience;
      const allIds: EnabledIds = {
        purposesConsent: getAllIds(experience.tcf_purpose_consents),
        purposesLegint: getAllIds(experience.tcf_purpose_legitimate_interests),
        specialPurposes: getAllIds(experience.tcf_special_purposes),
        features: getAllIds(experience.tcf_features),
        specialFeatures: getAllIds(experience.tcf_special_features),
        vendorsConsent: getAllIds([
          ...(experience.tcf_vendor_consents || []),
          ...(experience.tcf_system_consents || []),
        ]),
        vendorsLegint: getAllIds([
          ...(experience.tcf_vendor_legitimate_interests || []),
          ...(experience.tcf_system_legitimate_interests || []),
        ]),
      };
      onSave(ConsentMethod.ACCEPT, allIds);
    }
  };
  const handleRejectAll = () => {
    if (!experience.minimal_tcf) {
      const emptyIds: EnabledIds = {
        purposesConsent: [],
        purposesLegint: [],
        specialPurposes: [],
        features: [],
        specialFeatures: [],
        vendorsConsent: [],
        vendorsLegint: [],
      };
      onSave(ConsentMethod.REJECT, emptyIds);
    }
  };

  return (
    <ConsentButtons
      availableLocales={experience.available_locales}
      onManagePreferencesClick={onManagePreferencesClick}
      onAcceptAll={handleAcceptAll}
      onRejectAll={handleRejectAll}
      renderFirstButton={renderFirstButton}
      isInModal={isInModal}
      options={options}
      isTCF
      disableAll={experience.minimal_tcf}
    />
  );
};
