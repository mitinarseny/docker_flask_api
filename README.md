# Template API on Flask in Docker
> You can use this project architecture to easily build API on Flask in Docker.
## Usage
### Build
Run this in terminal from project root:
```bash
docker build -t <container_tag> .
```
### Run
Run this in terminal:
```bash
docker run \
-e JWT_SECRET_KEY=<secret_key> \
-e BUNDLE_API_ERRORS=<boolean> \
-p <host_port>:<containter_port> \
-t \
-i \
<containter_tag>
```
