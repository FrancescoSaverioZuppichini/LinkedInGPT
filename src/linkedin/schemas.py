from typing import Dict, List, Optional, Tuple, TypedDict


class ProfilePicture(TypedDict):
    displayImage: str


class LocalizedName(TypedDict):
    it_IT: str


class PreferredLocale(TypedDict):
    country: str
    language: str


class Name(TypedDict):
    localized: LocalizedName
    preferredLocale: PreferredLocale


class UserProfile(TypedDict):
    localizedLastName: str
    profilePicture: ProfilePicture
    firstName: Name
    lastName: Name
    id: str
    localizedFirstName: str


class ServiceRelationship(TypedDict):
    relationshipType: str
    identifier: str


class RegisterUploadRequest(TypedDict):
    recipes: List[str]
    owner: str
    serviceRelationships: List[ServiceRelationship]


class RegisterUploadBody(TypedDict):
    registerUploadRequest: RegisterUploadRequest


class UploadHttpRequest(TypedDict):
    uploadUrl: str
    headers: Dict[str, str]


class UploadMechanism(TypedDict):
    com_linkedin_digitalmedia_uploading_MediaUploadHttpRequest: UploadHttpRequest


class Value(TypedDict):
    mediaArtifact: str
    uploadMechanism: UploadMechanism
    asset: str
    assetRealTimeTopic: str


class RegisterUploadResponse(TypedDict):
    value: Value


class Text(TypedDict):
    text: str


class Title(TypedDict):
    text: str


class Description(TypedDict):
    text: str


class Media(TypedDict):
    status: str
    description: Description
    media: str
    title: Title


class ShareCommentary(TypedDict):
    text: str


class ShareContent(TypedDict):
    shareCommentary: ShareCommentary
    shareMediaCategory: str
    media: Optional[List[Media]]


class SpecificContent(TypedDict):
    com_linkedin_ugc_ShareContent: ShareContent


class MemberNetworkVisibility(TypedDict):
    com_linkedin_ugc_MemberNetworkVisibility: str


class CreatePostBody(TypedDict):
    author: str
    lifecycleState: str
    specificContent: SpecificContent
    visibility: MemberNetworkVisibility


class CreatePostResponse(TypedDict):
    id: str
