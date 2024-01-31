from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
    ]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=50, fields="nextPageToken, files(kind, driveId, fileExtension, copyRequiresWriterPermission, md5Checksum, contentHints, writersCanShare, viewedByMe, mimeType, exportLinks, parents, thumbnailLink, iconLink, shared, lastModifyingUser, owners, headRevisionId, sharingUser, webViewLink, webContentLink, size, viewersCanCopyContent, permissions, hasThumbnail, spaces, folderColorRgb, id, name, description, starred, trashed, explicitlyTrashed, createdTime, modifiedTime, modifiedByMeTime, viewedByMeTime, sharedWithMeTime, quotaBytesUsed, version, originalFilename, ownedByMe, fullFileExtension, properties, appProperties, isAppAuthorized, teamDriveId, capabilities, hasAugmentedPermissions, trashingUser, thumbnailVersion, trashedTime, modifiedByMe, permissionIds, imageMediaMetadata, videoMediaMetadata, shortcutDetails, contentRestrictions, resourceKey, linkShareMetadata, labelInfo, sha1Checksum, sha256Checksum)").execute()
        items = results.get('files', [])

        print(items)
        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
