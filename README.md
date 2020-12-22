# Nyaa-cli [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![nyaacli](https://img.shields.io/pypi/pyversions/nyaacli)](https://pypi.org/project/nyaacli/) [![nyaa.si](https://img.shields.io/badge/-nyaa.si-green)](https://nyaa.si)


A CLI for downloading Anime from https://nyaa.si making use of their RSS Feed and [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)

**Warning:** Only tested on Linux. Windows or MacOS support is not guaranteed, feel free to open issues about it, but I don't have any non-Linux machines to test any problems related to other OSes.

[CHANGELOG](CHANGELOG.md)

---

![image](https://user-images.githubusercontent.com/37747572/69002323-bb2ea100-08cb-11ea-9b47-20bd9870c8c0.png)

---

![image](https://user-images.githubusercontent.com/37747572/69002293-33e12d80-08cb-11ea-842e-02947726185d.png)

---

![image](https://user-images.githubusercontent.com/37747572/69002363-ad2d5000-08cc-11ea-9360-76bf1598512d.png)

---

## Installing

- `python3 -m pip install nyaacli --user`
  - *Note:* python-libtorrent will still need to be downloaded separately as shown below

- This Program depends on libtorrent together with its Python API, which can be installed using apt on debian-based linux distros with `sudo apt install python3-libtorrent` (`libtorrent-rasterbar` with pacman for Arch-based distros) or can be built from source here: [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)

---

## Usage

- **Help:** `nyaa --help` or `nyaa-cli --help`

```bash
Usage: nyaa [OPTIONS] ANIME [EPISODE]

  Search for Anime on https://nyaa.si and downloads it

  Usage:
      nyaa "Anime Name" <Episode Number (Optional)> -o <Output Folder (Default = "~/Videos/Anime")>

  Example:
      nyaa "Kimetsu no Yaiba" 19 -o /home/user/My/Animes/Folder/Kimetsu_No_Yaiba/

Options:
  -o, --output PATH     Output Folder  [default: ~/Videos/Anime]
  -n, --number INTEGER  Number of entries  [default: 10]
  -s, --sort-by TEXT    Sort by  [default: seeders]
  -t, --trusted         Only search trusted uploads
  -d, --debug           Debug Mode
  -c, --client          Use Torrent Client
  -p, --player          Open in Video Player after download
  --help                Show this message and exit.
```

- **Example:**
    ```bash
    # Downloading Episode 14 of 'Steins;gate' to '~/Anime/Steins;Gate'
    nyaa "Steins;Gate" 14 -o ~/Anime/Steins\;Gate
    ```

