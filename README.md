# Nyaa_cli

A CLI for downloading Anime from https://nyaa.si making use of their RSS Feed and [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)

---

![image](https://user-images.githubusercontent.com/37747572/69002323-bb2ea100-08cb-11ea-9b47-20bd9870c8c0.png)

![image](https://user-images.githubusercontent.com/37747572/69002293-33e12d80-08cb-11ea-842e-02947726185d.png)

![image](https://user-images.githubusercontent.com/37747572/69002363-ad2d5000-08cc-11ea-9360-76bf1598512d.png)

---

## Installing

- `python3 -m pip install nyaa_cli --user`
  - *Note:* python-libtorrent will still need to be downloaded separately as shown below

- This Program depends on python3-libtorrent, which can be installed using Apt with `sudo apt install python3-libtorrent` or can be built from source here: [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)

---

## Usage

- **Help:** `nyaa --help` or `nyaa-cli --help`

- `nyaa "Anime Name" <Episode Number (Optional)> -o <Output Folder (Default: ~/Videos/Anime)>`
  - **Example:**
    ```bash
    # Downloading Episode 14 of 'Steins;gate' to '~/Anime/Steins;Gate'
    nyaa "Steins;Gate" 14 -o ~/Anime/Steins\;Gate
    ```
  - Then select the entry you want to Download
