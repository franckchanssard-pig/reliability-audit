# Document360 API formats (from Swagger)

## API server base URLs
- `https://apihub.document360.io` (primary API hub)
- `https://apihub.us.document360.io` (US data center)
- `https://apihub.{private_hosting}.document360.io` (private hosting, replace `private_hosting` with your subdomain)

## Authentication
- Use an API token provided in the `api_token` header for every request.
- The token is generated in **Settings > Knowledge base portal > API tokens** and must match the workspace/permissions you need.

## Core resource groups (v2)
The OpenAPI spec exposes these top-level resource groups under `/v2/`:
- `APIReferences`
- `Articles`
- `Categories`
- `Drive`
- `Language`
- `Project`
- `ProjectVersions`
- `Readers`
- `Teams`
- `Translations`

## Example request formats
### 1) Fetch an article by URL
```bash
curl -sS \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  "https://apihub.document360.io/v2/Articles?url=/workspace/docs/en/article-slug&applyRedirection=true&isForDisplay=true"
```

### 2) List categories
```bash
curl -sS \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  "https://apihub.document360.io/v2/Categories"
```

### 3) List project versions
```bash
curl -sS \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  "https://apihub.document360.io/v2/ProjectVersions"
```

## Notes
- Swagger UI is available at https://apihub.document360.io/index.html and references the OpenAPI documents at:
  - `https://apihub.document360.io/swagger/v2/swagger.json` (Document360 Customer API v2)
  - `https://apihub.document360.io/swagger/v1/swagger.json` (Customer API v1)
