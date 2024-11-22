class Configuration():
    appname: str
    account: str
    region: str

    AthenaRegion: str
    AthenaDatabase: str
    AthenaWorkgroup: str
    AthenaResultsBucket: str
    CognitoUserPoolId: str

    def __init__(self, appname, account, region, AthenaRegion, AthenaDatabase, AthenaWorkgroup,
                 AthenaResultsBucket, AppSyncApiUrl, CognitoUserPoolId) -> None:
        self.appname = appname
        self.account = account
        self.region = region
        self.AthenaRegion = AthenaRegion
        self.AthenaDatabase = AthenaDatabase
        self.AthenaWorkgroup = AthenaWorkgroup
        self.AthenaResultsBucket = AthenaResultsBucket
        self.AppSyncApiUrl = AppSyncApiUrl
        self.cognito_user_pool_id = CognitoUserPoolId

