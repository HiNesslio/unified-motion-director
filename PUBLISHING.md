# Publishing the repository

This package contains a full GitHub-ready source tree. It is not yet proof that the files have been uploaded.

To publish under the GitHub account connected to ChatGPT (`HiNesslio`):

1. Open https://github.com/new and create an empty repository named `unified-motion-director` under `HiNesslio`. Choose your desired visibility. Do not add GitHub's starter README, .gitignore or license, because this package already includes them.
2. Extract the archive and open a terminal in the extracted `unified-motion-director` folder.
3. Push with your authenticated GitHub credentials:

```bash
git init -b main
git add .
git commit -m "Publish Unified Motion Director v1.6"
git remote add origin https://github.com/HiNesslio/unified-motion-director.git
git push -u origin main
```

Alternatively, once the empty repository exists and the GitHub connector has write access, ask ChatGPT to finish publishing the source tree.

Do not publish third-party downloaded footage, music, source clones or tokens along with this repository. Keep the `.gitignore` intact.