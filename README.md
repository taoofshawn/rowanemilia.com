# [rowanemilia.com](https://www.rowanemilia.com/) hugo blog 

### Links
- [github repo](https://github.com/taoofshawn/rowanemilia.com)
- [gh actions](https://github.com/taoofshawn/rowanemilia.com/actions)
- [gh container registry](https://github.com/taoofshawn/rowanemilia.com/pkgs/container/rowanemilia.com)
- [rowanemilia.com](https://www.rowanemilia.com/)

### Notes

- converted from wordpress, trying out a different agent
  - [pi agent](https://pi.dev/)
  - [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
  - [karpathy CLAUDE.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md)
  - [superpowers](https://github.com/obra/superpowers.git)

- git actions for building and pushing the container image. for some reason I had a difficult time finding these steps in one place
    - setup a [classic personal access token](https://github.com/settings/tokens)
        - give permission `write:packages`
    - add to repository secrets (repo > settings > secrets and variables > actions > new repository secret)
        - named `GHCR_TOKEN` to match the .github/workflows/docker-image.yml in this repository
