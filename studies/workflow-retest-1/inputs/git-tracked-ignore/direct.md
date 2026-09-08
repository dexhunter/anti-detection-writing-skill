Remove the file from Git's index, then commit that removal along with your ignore rule. From the repository root:

```sh
git rm --cached -- config.local.json
git add .gitignore
```

The `--cached` option keeps your local copy on disk. After you commit, the repository no longer tracks the file, and the rule in `.gitignore` prevents ordinary `git add` from adding it again.

Adding the ignore rule alone did not work because `.gitignore` applies only to untracked files. It cannot stop tracking a file you have already committed. See the [Git documentation](https://git-scm.com/docs/gitignore/2.42.0#_notes).
