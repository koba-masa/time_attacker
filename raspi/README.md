## 動作環境
- `python3.9.2`

### 動作環境構築
```sh
$ sudo pip3 install poetry
$ sudo apt-get install python3-dev python3-setuptools
$ sudo apt-get install libjpeg-dev
```

### 配線図(ブレッドボード)
![配線図](doc/images/bread_board.jpg)

### 起動コマンド
```sh
$ cd raspi
$ poetry install
$ poetry run python3 raspi/time_attacer
```

#### 自動起動設定
1. 以下のファイルを開く
   - `/etc/rc.local`
2. 以下を記載する
   - `sudo -u <ユーザ> python3 <配置場所>/play_with_raspberry_pi/python/src/time_attacker.py &`
