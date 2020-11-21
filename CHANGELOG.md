# Changelog

---

## 0.2.3

- Add `--client` / `-c` flag to open torrent file with default Torrent Client instead of using Libtorrent

---

## 0.2.2

- Fix issue with not being able to correctly get resolution from torrent entry title

---

## 0.2.1

- Fixed issue where torrent selection was actually in some cases selecting the torrent above the one selected

---

## 0.2.0

- Only show torrent alert messages in debug mode (`--debug`) (Closes Issue [`#25`](https://github.com/johnvictorfs/nyaa-cli/issues/25))

- Add argument to search for only trusted torrents `-t` (`--trusted`) (Closes Issue [`#26`](https://github.com/johnvictorfs/nyaa-cli/issues/26))

- Add argument alias for `--debug` (`-d`)

- Removed off-switch for `--debug` flag (used to be `--no-debug`). It's already off by default so it was an useless argument

- Add option to sort by different values other than seeders with `--sort-by` (`-s`). (Closes Issue [`#27`](https://github.com/johnvictorfs/nyaa-cli/issues/27)). See linked issue to see options available.

---

## 0.1.8

- Add argument `-n` (`--number`, default = 10) to specify the number of entries to select from ([`#24`](https://github.com/johnvictorfs/nyaa-cli/commit/53771685f94f2d34c257b45c2ca749b08ab18ac2))

---

## 0.1.7

- Fix issue when searching for specific episode numbers [`(f1ac2e9)`](https://github.com/johnvictorfs/nyaa-cli/commit/f1ac2e983fdb72c7a608d6c20d149ac1cb94dfa0)

---

## 0.1.6

- Update PyInquirer to forked version to fix issue with searching for Anime with broken 'regex' package [`(4346468)`](https://github.com/johnvictorfs/nyaa-cli/commit/434646855683b69f5def77b9f03bc75819aa9d89)

- Switch PyInquirer entirely with [questionary](https://github.com/tmbo/questionary) [`(f388427)`](https://github.com/johnvictorfs/nyaa-cli/commit/f388427e77974892696c62812478288a4690f5a6) (Closes Issue #20)

---

## 0.1.5

- Fix issue where selecting no Episodes when searching barely got any selections [`(697978b)`](https://github.com/johnvictorfs/nyaa-cli/commit/697978bd40d9524f74711d97bee06a8387d99411)
- Add published date next to Episode selection entries [`(697978b)`](https://github.com/johnvictorfs/nyaa-cli/commit/697978bd40d9524f74711d97bee06a8387d99411)

---

## 0.1.4

- Add Windows Support [`(b609d2f)`](https://github.com/johnvictorfs/nyaa-cli/commit/b609d2f05c0b2bb1a42b9654f380d38ab4219df6) (Closes Issue #10)
- Fix Entries in list re-appearing [`(b609d2f)`](https://github.com/johnvictorfs/nyaa-cli/commit/b609d2f05c0b2bb1a42b9654f380d38ab4219df6) (Closes Issue #7)
- Can now exit gracefully from List of entries with <kbd>Ctrl</kbd> + <kbd>C</kbd> [`(b609d2f)`](https://github.com/johnvictorfs/nyaa-cli/commit/b609d2f05c0b2bb1a42b9654f380d38ab4219df6) (Closes Issue #4)

---

## 0.1.3

- Terminal now clears after anime entry selection and after Video download ends [`(d9b0423)`](https://github.com/johnvictorfs/nyaa-cli/commit/d9b04232ee4ccfd9292cb46722e5403f1d0b49e0)

---

## 0.1.2

- Added the `nyaa` alias to the `nyaa-cli` command [`(2ca861b)`](https://github.com/johnvictorfs/nyaa-cli/commit/2ca861b6dcdffaa0cdf1556c2898e7a4a95c2bd6)

---

## 0.1.1

- Added the `nyaa-cli` command and uploaded the CLI to PyPi [`(7dae039)`](https://github.com/johnvictorfs/nyaa-cli/commit/7dae0396db018250683d40f8ce3343b4da8f2c23)

---

## 0.1.0

- Added CLI Interface for downloading anime from nyaa.si [`(7431796)`](https://github.com/johnvictorfs/nyaa-cli/commit/7431796d56b0c46e3d3b113d34bcb1847b952bf5)
