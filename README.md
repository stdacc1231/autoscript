# Autoscript

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux-0f172a?style=for-the-badge&logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Core-Xray-111827?style=for-the-badge&logo=radar&logoColor=white" alt="Xray">
  <img src="https://img.shields.io/badge/Edge-Go%20edge--mux-0b5fff?style=for-the-badge&logo=go&logoColor=white" alt="Go edge-mux">
  <img src="https://img.shields.io/badge/Remote-Telegram-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/WARP-Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Cloudflare WARP">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Manage-CLI-1f2937?style=flat-square&logo=gnubash&logoColor=white" alt="Manage CLI">
  <img src="https://img.shields.io/badge/Portal-Account-2563eb?style=flat-square&logo=vercel&logoColor=white" alt="Account Portal">
  <img src="https://img.shields.io/badge/Access-SSH%2FWebSocket-0ea5e9?style=flat-square&logo=protonvpn&logoColor=white" alt="SSH WebSocket">
  <img src="https://img.shields.io/badge/Utility-BadVPN-475569?style=flat-square&logo=wireguard&logoColor=white" alt="BadVPN">
  <img src="https://img.shields.io/badge/Service-ZIVPN-16a34a?style=flat-square&logo=shield&logoColor=white" alt="ZIVPN">
  <img src="https://img.shields.io/badge/Support-Backup%20%26%20Restore-0f766e?style=flat-square&logo=icloud&logoColor=white" alt="Backup and Restore">
  <img src="https://img.shields.io/badge/Zero%20Trust-Cloudflare%20WARP-F38020?style=flat-square&logo=cloudflare&logoColor=white" alt="Cloudflare WARP">
</p>

## Fokus

- `autoscript` = repo utama untuk stack VPS lengkap
- `run.sh` = bootstrap host
- `manage` = panel operasi harian
- `Xray`, `SSH/WebSocket`, `ZIVPN`, `BadVPN`, `WARP`
- `Account Portal`, `Bot Telegram`, `Backup/Restore`, `Domain Guard`, `Uninstall`

## Status Biaya

Source code `autoscript` tersedia gratis untuk digunakan.

Aktivasi lisensi IP VPS tetap menjadi bagian dari flow produk. Namun, repositori dan source code `autoscript` sendiri bukan software berbayar.

## Persiapan Sebelum Install

Sebelum menjalankan installer, aktifkan lisensi IP VPS terlebih dahulu:

- Website lisensi: `https://autoscript.license.dpdns.org`
- Langkah singkat:
  1. buka website lisensi
  2. input public IPv4 VPS
  3. selesaikan verifikasi bila diminta
  4. pastikan IP sudah aktif
  5. jalankan `run.sh`

Jika lisensi belum aktif, installer akan berhenti pada tahap preflight `License Guard`.

## Quick Install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/superdecrypt-dev/autoscript/main/run.sh)
```

## Arsitektur Singkat

```text
Internet / Cloudflare
        |
        v
  edge-mux (Go)
  :80, :8080, :8880, :2052, :2082, :2086, :2095
  :443, :2053, :2083, :2087, :2096, :8443
        |
        +--> nginx            127.0.0.1:18080
        +--> SSH Dropbear     127.0.0.1:22022
        +--> SSH Stunnel      127.0.0.1:22443
        +--> WS Proxy (Go)    127.0.0.1:10015
        +--> Xray-core        via inbound runtime
```

## Kapabilitas Utama

### Layanan inti

- `Xray` untuk `VLESS`, `VMess`, dan `Trojan`
- `SSH Direct`, `SSH SSL/TLS`, dan `SSH WS`
- `ZIVPN`
- `BadVPN UDPGW`
- `WARP Free/Plus` dan `WARP Zero Trust`

### Transport Xray

- `VMess TCP+TLS`
- `VLESS XHTTP3`
- `VLESS WS`
- `VLESS HUP`
- `VLESS XHTTP`
- `VLESS gRPC`
- `VLESS TCP+TLS`
- `VMess WS`
- `VMess HUP`
- `VMess XHTTP`
- `VMess gRPC`
- `VMess TCP+TLS`
- `Trojan WS`
- `Trojan HUP`
- `Trojan XHTTP`
- `Trojan gRPC`
- `Trojan TCP+TLS`

### Tooling operator

- `manage` CLI modular
- `Account Portal`
- `Bot Telegram`
- `Backup/Restore`
- `License Guard`
- `Domain Guard`
- `Traffic`, `QAC`, `Speed`, dan `Adblocker`
- `Tools > Uninstall` untuk teardown total stack autoscript

## Komponen Runtime

| Komponen | Peran | Status |
| --- | --- | --- |
| `edge-mux` | ingress publik utama | frontend |
| `xray` | core proxy utama | backend |
| `nginx` | HTTP backend internal dan web support | internal |
| `sshws-dropbear` | backend SSH direct | internal |
| `sshws-stunnel` | backend SSH TLS | internal |
| `sshws-proxy` | backend SSH WebSocket | internal |
| `badvpn-udpgw` | UDPGW lokal | internal |
| `wireproxy` / `warp-svc` | runtime WARP | sesuai mode aktif |
| `zivpn` | backend UDP ZIVPN | internal |
| `account-portal` | portal akun read-only | opsional |
| `bot-telegram-backend` | API internal bot | opsional |
| `bot-telegram-gateway` | gateway Telegram | opsional |
| `xray-domain-guard` | guard domain dan TLS | maintenance |
| `xray-session` | pelacak sesi aktif Xray | maintenance |

## Eksposur Jaringan

### Port publik edge gateway

| Kategori | Port | Keterangan |
| --- | --- | --- |
| `HTTP primary` | `80` | ingress utama |
| `HTTP alternate` | `8080, 8880, 2052, 2082, 2086, 2095` | port alternatif |
| `HTTPS primary` | `443` | ingress utama TLS |
| `HTTPS alternate` | `2053, 2083, 2087, 2096, 8443` | port alternatif |

### Ekspos layanan

| Layanan | Port user-facing |
| --- | --- |
| `SSH WS` | `443, 80` + alt port |
| `SSH SSL/TLS` | `443, 80` + alt port |
| `SSH Direct` | `443, 80` + alt port |
| `VLESS` semua transport | `443, 80` + alt port |
| `VMess` semua transport | `443, 80` + alt port |
| `Trojan` semua transport | `443, 80` + alt port |

## Path Publik Stabil

Gunakan hanya path publik di bawah ini untuk client. Hindari memakai path internal acak backend lokal.

| Transport | Path utama | Varian alt | Catatan |
| --- | --- | --- | --- |
| `SSH WS` | `/<token-hex-10>` | `/<bebas>/<token-hex-10>/<bebas>` | token SSH WS 10 digit heksadesimal |
| `VLESS WS` | `/vless-ws` | `/<bebas>/vless-ws/<bebas>` | path publik stabil |
| `VLESS HUP` | `/vless-hup` | `/<bebas>/vless-hup/<bebas>` | path publik stabil |
| `VLESS XHTTP` | `/vless-xhttp` | `/<bebas>/vless-xhttp/<bebas>` | path publik stabil |
| `VLESS XHTTP3` | `xray.json per akun` | mengikuti profile UDP/QUIC | profile client dirender otomatis |
| `VLESS gRPC` | `/vless-grpc` | `/<bebas>/vless-grpc/<bebas>` | service name internal disembunyikan |
| `VMess WS` | `/vmess-ws` | `/<bebas>/vmess-ws/<bebas>` | path publik stabil |
| `VMess HUP` | `/vmess-hup` | `/<bebas>/vmess-hup/<bebas>` | path publik stabil |
| `VMess XHTTP` | `/vmess-xhttp` | `/<bebas>/vmess-xhttp/<bebas>` | path publik stabil |
| `VMess gRPC` | `/vmess-grpc` | `/<bebas>/vmess-grpc/<bebas>` | service name internal disembunyikan |
| `Trojan WS` | `/trojan-ws` | `/<bebas>/trojan-ws/<bebas>` | path publik stabil |
| `Trojan HUP` | `/trojan-hup` | `/<bebas>/trojan-hup/<bebas>` | path publik stabil |
| `Trojan XHTTP` | `/trojan-xhttp` | `/<bebas>/trojan-xhttp/<bebas>` | path publik stabil |
| `Trojan gRPC` | `/trojan-grpc` | `/<bebas>/trojan-grpc/<bebas>` | service name internal disembunyikan |

Catatan:

- `TCP+TLS` tidak menggunakan path publik
- `VLESS XHTTP3` menggunakan profile `xray.json` yang dirender per akun

## Port Internal

| Komponen | Bind | Keterangan |
| --- | --- | --- |
| `nginx` | `127.0.0.1:18080` | backend web internal |
| `sshws-dropbear` | `127.0.0.1:22022` | backend SSH direct |
| `sshws-stunnel` | `127.0.0.1:22443` | backend SSH TLS |
| `sshws-proxy` | `127.0.0.1:10015` | backend SSH WS |
| `account-portal` | `127.0.0.1:7082` | website info akun |
| `bot-telegram-backend` | `127.0.0.1:7081` | API internal bot |
| `edge-mux metrics` | `127.0.0.1:9910` | metrics edge |
| `WARP local proxy` | `127.0.0.1:40000` | runtime Zero Trust |
| `BadVPN UDPGW` | `127.0.0.1:7300, 7400, 7500, 7600, 7700, 7800, 7900` | UDPGW lokal |

## Account Portal

Setiap akun `Xray` dan `SSH` dapat memiliki link portal read-only sendiri.

- format URL:
  - `https://<domain-vps>/account/<token>`
- portal menampilkan:
  - status akun
  - masa aktif
  - quota limit, used, dan remaining
  - sesi aktif yang masih terdeteksi runtime
- endpoint JSON:
  - `GET /api/account/<token>/summary`

Untuk `VLESS XHTTP3`, portal juga dapat menyediakan file profile `xray.json` bila akun memiliki artefak tersebut.

## Manage CLI

### Menu utama

```text
1) Xray Users
2) SSH Users
3) Xray QAC
4) SSH QAC
5) Xray Network
6) SSH Network
7) Adblocker
8) Domain Control
9) Speedtest
10) Security
11) Maintenance
12) Traffic
13) Tools
0) Keluar
```

### Menu `Tools`

```text
13) Tools
1) Telegram Bot
2) WARP Tier
3) License Guard
4) Backup/Restore
5) Uninstall
0) Back
```

### Menu `Uninstall`

```text
13) Tools > Uninstall
1) Full Hard Uninstall
0) Back
```

`Full Hard Uninstall` ditujukan untuk membersihkan stack autoscript secara keras, termasuk service, unit, akun managed, cert/domain lokal, secret bot, config backup, dan runtime state. Package sistem tetap dibiarkan terpasang.

## WARP

### WARP Xray

`Xray Network -> WARP` mendukung override per-user dan per-inbound:

- `direct`
- `warp`
- `reset ke global`

### WARP SSH

- `SSH Network` mendukung WARP host/global dan mode per-user
- backend dapat mengikuti `wireproxy` atau `Zero Trust` sesuai state aktif

## Cloudflare Zero Trust Setup

Bagian ini dipakai saat Anda ingin menyiapkan `WARP Zero Trust` dengan service token.

### 1) Device enrollment permissions

Masuk ke:

`Team & Resources -> Devices -> Management -> Device enrollment permissions -> Manage -> Policies`

Lalu:

1. add rule `Policies`
2. nama bebas
3. `Rule action`: `service auth`
4. `Include selector`: `Any Access Service Token`
5. save

### 2) Device Profile

Masuk ke:

`Team & Resources -> Devices -> Device Profile`

Lalu:

1. `Create new profile`
2. nama bebas
3. selector -> `user email`
4. operator -> `is`
5. value: `non_identity@<team-name>.cloudflareaccess.com`
6. `+ AND condition`
7. selector -> `operating system`
8. operator -> `is`
9. value: `Linux`
10. `Device tunnel protocol`: `MASQUE`
11. `Service mode`: `local proxy mode port 40000`
12. save
13. lalu save sekali lagi

### 3) Service Token

Masuk ke:

`Access controls -> Service Credentials -> Service Token`

Lalu:

1. create service token
2. nama bebas
3. token durasi bebas
4. generate token
5. copy `Client ID` token dan `Client Secret` token

Catatan:

- Untuk enrollment headless Linux, `Device enrollment permissions` dengan `Service Auth` adalah bagian penting.
- `Device Profile` di atas dipakai sebagai pelengkap konfigurasi client, bukan pengganti service token.
- Pada host, kredensial biasanya dipakai oleh file `mdm.xml` di `/var/lib/cloudflare-warp/mdm.xml` dan config Zero Trust di `/etc/autoscript/warp-zerotrust/config.env`.

## Backup and Restore

`Backup/Restore` tersedia di:

- CLI `manage` lewat `13) Tools -> 4) Backup/Restore`
- bot Telegram lewat menu backup

Provider yang didukung:

- `Google Drive`
- `Cloudflare R2`
- `Telegram` untuk upload backup lokal dan restore file dari chat

Format nama backup manual:

- `backup-YYYY-MM-DD-HH:MM.tar.gz`

### Menu cloud

```text
- Setup
- Status Config
- Test Remote
- Create & Upload Backup
- List Cloud Backups
- Restore Latest Cloud Backup
- Restore Select Backup
- Delete Cloud Backup
```

### Perilaku restore

- restore cloud penuh bekerja sebagai `snapshot replace`
- domain aktif, config Xray, quota, speed, cert, dan state runtime dalam scope restore akan ikut dipulihkan
- sebelum restore penuh, sistem membuat `safety backup`
- bila validasi pasca-restore gagal, sistem mencoba rollback otomatis

Panduan detail tersedia di:

- `docs/BACKUP_RESTORE_CLOUD.md`

## Bot Telegram

Entry point utama:

- `/menu`
- `/cleanup`
- `/start`

Karakter bot:

- menu-first
- aman untuk operasi jarak jauh yang konservatif
- memakai ACL admin Telegram untuk aksi mutasi

Detail lanjutan tersedia di:

- `bot-telegram/README.md`

## Struktur Repo Penting

- `run.sh` dan `setup.sh`
  - bootstrap dan install host
- `manage.sh`
  - CLI operasional utama
- `opt/manage/`
  - modul CLI
- `opt/setup/`
  - installer, template, helper runtime
- `opt/edge/go/`
  - source `edge-mux`
- `opt/edge/dist/`
  - binary prebuilt `edge-mux`
- `account-portal/`
  - portal akun
- `bot-telegram/`
  - backend dan gateway Telegram
- `manage_bundle.zip`
  - artifact bundle installer/manage
- `bot_telegram.zip`
  - artifact bundle bot

## Catatan Operasional

- gunakan path publik stabil untuk client
- hindari memakai path internal acak backend
- restore bersifat live dan dapat menimpa runtime aktif
- `Tools > Uninstall` bersifat destruktif dan ditujukan untuk teardown total stack

## Summary

Jika Anda membutuhkan satu repositori yang dapat:

- menginstal VPS dari nol
- menyediakan layanan `Xray`, `SSH`, `ZIVPN`, dan `WARP`
- memberikan panel CLI yang kuat untuk operasi harian
- menyediakan portal akun dan bot Telegram
- tetap nyaman dipakai untuk maintenance, troubleshooting, dan recovery

maka `autoscript` memang dibangun untuk kebutuhan tersebut, dengan tampilan yang lebih rapi dan pengalaman operasional yang tetap solid.
