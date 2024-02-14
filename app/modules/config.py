class AppConfig(object):
    # セッション Cookie に安全に署名するために使用される秘密キー
    SECRET_KEY = 'fbc0b8ddc8deba4769b780a959405de3370c883f6c6b47499487e364e17b24a1'

    # セッション Cookieの名前
    SESSION_COOKIE_NAME = 'flask_login_app'

MOCK_SHIB_DATA={"testuser1A@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser1A",
                                        "OrganizationName":"alpha",
                                        "wekoSocietyAffiliation":"",
                                        "eduPersonOrcid":"orcid_testuser1"},
                "testuser2A@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser2A",
                                        "OrganizationName":"alpha",
                                        "wekoSocietyAffiliation":"",
                                        "eduPersonOrcid":"orcid_testuser2"},
                "testuser3A@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser3A",
                                        "OrganizationName":"alpha",
                                        "wekoSocietyAffiliation":"図書館員",
                                        "eduPersonOrcid":""},
                "testuser1B@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.betabeta.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser1B",
                                        "OrganizationName":"beta",
                                        "wekoSocietyAffiliation":"",
                                        "eduPersonOrcid":"orcid_testuser1"},
                "testuser2B@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.betabeta.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser2B",
                                        "OrganizationName":"beta",
                                        "wekoSocietyAffiliation":"",
                                        "eduPersonOrcid":"orcid_testuser2"},
                "testuser3B@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.betabeta.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                        "eduPersonPrincipalName":"testuser3B",
                                        "OrganizationName":"beta",
                                        "wekoSocietyAffiliation":"図書館員",
                                        "eduPersonOrcid":""},
                "testadmin@nii.ac.jp":{"affiliation_idp_url":"https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO",
                                       "eduPersonPrincipalName":"testuser4",
                                        "OrganizationName":"alpha",
                                        "wekoSocietyAffiliation":"管理者",
                                        "eduPersonOrcid":""}}