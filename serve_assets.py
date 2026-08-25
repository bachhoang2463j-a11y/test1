#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my_assets 局域网静态资源服务 — Threading + CORS/CORP
对标 C:\\Users\\ELevin\\Downloads\\酒馆BGM 的简易托管，但补齐：
  - ThreadingHTTPServer：预加载 30 并发 + 群增/三连发首响不排队
  - CORS/CORP/Accept-Ranges/Cache：让 JS-Slash-Runner iframe 跨域 fetch(blob) 与 video.crossOrigin='anonymous'+canvas 可播
  - MIME：.webm/.mp4/.mp3/.wav 显式注册

用法：
  python serve_assets.py --port 8766 --host 0.0.0.0 --dir "D:\\Project\\my_assets"
  默认托管本文件所在目录，端口 8766，监听 0.0.0.0 供局域网手机/PC 共同访问。
  RpgCombat 侧 ASSET_ORIGIN 指向 http://192.168.110.83:8766 即可（根即 my_assets，无需再拼 /my_assets）。
"""

import argparse
import mimetypes
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# 显式注册媒体 MIME，避免系统缺失导致 Content-Type: application/octet-stream
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("audio/mpeg", ".mp3")
mimetypes.add_type("audio/wav", ".wav")
mimetypes.add_type("audio/ogg", ".ogg")


class CORSHandler(SimpleHTTPRequestHandler):
    """为局域网跨域播放注入必要响应头。"""

    def __init__(self, *args, directory=None, **kwargs):
        # directory 指向 my_assets 根；不传则取本文件所在目录
        if directory is None:
            directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        # JS-Slash-Runner iframe 的 fetch(blob) / video.crossOrigin='anonymous' / AudioContext 均需通过
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type")
        self.send_header("Access-Control-Expose-Headers", "Content-Length, Content-Range, Accept-Ranges")
        # 供 CORP 校验（video.crossOrigin + canvas getImageData）；与 helmet CORP:same-origin 对齐放宽
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "public, max-age=86400")
        # 中文文件名在旧版 SimpleHTTPRequestHandler 可能缺 charset，补 utf-8
        super().end_headers()

    def do_OPTIONS(self):
        # 预检直接 204，无需 body
        self.send_response(204)
        self.end_headers()


def parse_args():
    ap = argparse.ArgumentParser(description="my_assets Threading+CORS static server")
    ap.add_argument("--port", type=int, default=8766, help="监听端口 (默认 8766，避开 8000/8083/8766)")
    ap.add_argument("--host", default="0.0.0.0", help="监听地址 (默认 0.0.0.0 供局域网访问)")
    ap.add_argument("--dir", dest="directory", default=None, help="托管目录 (默认本文件所在目录 D:\\Project\\my_assets)")
    return ap.parse_args()


def main():
    args = parse_args()
    serve_dir = args.directory
    if serve_dir is None:
        serve_dir = os.path.dirname(os.path.abspath(__file__))
    serve_dir = os.path.abspath(serve_dir)
    if not os.path.isdir(serve_dir):
        print(f"[my_assets] 目录不存在: {serve_dir}", file=sys.stderr)
        sys.exit(1)

    # 允许快速重启（避免 TIME_WAIT 占端口）
    ThreadingHTTPServer.allow_reuse_address = True
    # ThreadingHTTPServer 继承 ThreadingMixIn.daemon_threads=True，Ctrl+C 可干净退出

    handler_factory = lambda *a, **k: CORSHandler(*a, directory=serve_dir, **k)

    addr = (args.host, args.port)
    with ThreadingHTTPServer(addr, handler_factory) as httpd:
        host_disp = "127.0.0.1" if args.host == "0.0.0.0" else args.host
        # 友好提示：局域网 IP 需用户自行确认，本机 192.168.110.83 为例
        print("=" * 60)
        print("  my_assets 本地资源服务器已启动 (Threading + CORS/CORP)")
        print("=" * 60)
        print(f"  目录: {serve_dir}")
        print(f"  本机: http://{host_disp}:{args.port}/  (局域网请用 http://192.168.110.83:{args.port}/)")
        print(f"  示例: http://192.168.110.83:{args.port}/hitUp.mp3")
        print(f"  中文示例: http://192.168.110.83:{args.port}/%E7%B4%A2%E6%81%A9/xxx.mp3")
        print("  请勿关闭此窗口（可最小化）；手机/PC 酒馆均通过它跨域拉取资源。")
        print("  按 Ctrl+C 停止。")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[my_assets] 已停止。")


if __name__ == "__main__":
    main()
