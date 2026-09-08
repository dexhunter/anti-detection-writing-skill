From the repository root, use `--cached` to remove `config.local.json` from Git's index while leaving your local copy on disk:

```sh
git rm --cached -- config.local.json
git add .gitignore
```

Keep `/config.local.json` in `.gitignore` and commit the tracking removal together with that rule. Ignore rules only affect untracked files, which is why adding the rule alone did not stop the changes appearing. The repository will no longer track the file; the rule prevents ordinary `git add` from adding it again.

See the [Git documentation](https://git-scm.com/docs/gitignore/2.42.0#_notes).