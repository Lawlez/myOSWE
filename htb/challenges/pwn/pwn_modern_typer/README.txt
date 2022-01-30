The Chrome version is 88.0.4324.182. You can `git reset --hard 88.0.4324.182` in a Chromium source repo to get the correct version.

The remote server will run Chrome like this:

`./chrome --headless --disable-gpu --user-data-dir=/tmp/nonexistent --no-sandbox <link you provide>`

Please ensure your exploit works locally with the same Chrome binary (and the same flags as above) before attempting to run it against the remote server.
