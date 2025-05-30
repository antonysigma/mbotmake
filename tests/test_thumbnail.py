from parsimonious.grammar import Grammar

from mbotmake2.grammars.thumbnails import grammar
from mbotmake2.transformers.thumbnails import PNGImage, ThumbnailDecoder

thumbnail_raw = r"""
;
; thumbnail begin 55x40 2736
; iVBORw0KGgoAAAANSUhEUgAAADcAAAAoCAYAAABaW2IIAAAHyUlEQVR4Ae1ZW09UVxQ+f6GV68wAA2
; MrrUi1rdaW1hgvGAFFxduIAqIjIBcZLoogiFw0ggS8EJTgLUpMTNTE2JDeEtM21pja1Afb0MbUpCbl
; oQ8+kPAwD7vr286abI/nxjwYTPqwc2bOOfvs79vr+9ba+xxt6dKlQm2VlZXPhoaGHuAYCAQmrly58j
; 1+6+9TW3Z2dqitrW18YGDgYUFBwWRTU9OT8+fP38Nvq35+v/85xkJf/Eb/np6eR3ieVT8jjMFg8Kn+
; Ps2oM0DduXNnDJ0wqNVAagOpsbGxLzGw0z4gMjIycu/27dtfgaTTfoxxdHT0rhlGzagTwDU3N//JES
; guLv7XbjDMIiajpqbm766urseIQF5e3pQdMdyLiGEMjoZd5PQY8dsI40vkEFo9GZYOHmI0KM6BCAAy
; GZyzGpSfi7Fwn56s1cRMB6PGM2Gld72n+LyV3vWeUp/LijCTk+opNVrTxahBRk6SBpPhQY3ImkkPZH
; BveXn5P0zWbiyVTLQYtevXr3/npJPaGUkDg9l5Sm2QGxKAk2zIDc+/du3a3WgwYiyNUzCkZTco6x2d
; 7TylRo49iWg4TTa4lz1p53szjBoD4EGNZGamd7tBzTzJnsJ1I4BGnjTzvRVGzUyvKhArvaueUgfVA1
; mUmyu+WLZMfJ6TIxuDwaQyGD5n5cnpYNTMZqCvr+9XBujEWxzFhoaGvziafO3j5ctFQn6+mL1tm8jK
; zhbvlZaKJStWvFQyWltb/wBAs2jqMSJCKkajaGpmQGFIpwVclRNWGgCLCVlCpOb7/SKLjp9R1GZv3S
; o81dXC09Qk5tTVRQgODg4+uHHjxrdOPKXHePHixR/NMGpWendqZL3e2VPLy8qev0USnLVxo3BRtDI2
; bRLe3bsluaRDh8TCoqIpjMXJzMr30WDU9AD1erczspnece8xAhpsaRmPXbtWxBOphL17X0Tu4EHhbm
; gQKX5/SP9MowLuBKOR7zUVoJXe9Ws/O9IfFhSI1NrakK++PuQiCcaVlEiCaO7GRoFziTU1Yl4gYKkE
; 9rsTjBxFxqjBlE6TBu6BdPr7+3/RJw21wWsA7woGRUJ5uYgrLhYJFRUisapKxBYVCU9zsySYfPiwcN
; M9i+l+/TM4GufOnbs/HYwsb2DUsN2YjpERLU4aZrOIjDh3+3aRSXJ0ZWWJt/LyREJZmXDt2ycSKyul
; 3yDR5PZ2SfyDVatMI4EVSjQYb9269bVmJy8zvfPKRr8oRtTep5QP8G6KVgodE8lniTgSMXgtkUgiko
; haDGXQFEowi2gC9EmDMU0XI9dOjS+oxVE/Q2Z6V43M6TidIgE5wk8gIaVJxBA5NEgyjqQJ2Xo7O6VM
; U0+eFD7KqAzQTPJWez4jjJqeubr2UzeTVnrnKGKAjLKyEAhBgq7aWim7GKp1IOamCOGIc94TJ4Svp0
; d4DhwQPiIXS9HeVlU1wetCO987waiZGfny5cs/cA1yonP0C7S1PZ3b2DgFUoicPBJJkJHZkX7H79ol
; Sab29Ql3fb3wUlLx0GTgno8qKiadJg3gAkYUcTOMmtFJkBseHv7JyFNmLSc/f0pGLNwkOSKDgo0sKV
; s4minHj0v/wXdplFRitmwRbro/fudOkZWb6yhpMMbTp0//bIbxFVmqejfylFGDHNd0dU1IYgQ+EjmQ
; JFLxe/a8KOCUJb0kRSQV1DsPRS5zZEQmlbkXLogkkuiCkpJJq/co08EYIafug4w8ZWRk1vuJoaGHIB
; JPSyyZGZVkklFdPZVcVBRCIvFSxLy9vTJSuJY+PCzmXbok3NRn/tWrIp4KPZZq1d3d40Z7PoxvhZF9
; H9ny4AdO2iUN/csbfsGDSeEMiQiBFMghUjgu7OiYTKasmNTWJtz798vzIJd26pR49+xZkULXvCRdH3
; kvlhIPrs0pKIjsFkDE6CWUE4zyNYPTpMGzd/PmzW/4pSsKdsRrkCQdsfqQi2MiBCkyYUmaVixJra0i
; bWDgRZkg33lprYnyAHJo81avjkQDu4VoMWrt7e2/23lKr/fOzs7feO2XGQiEIkkk7DX2m4wmrR0RUR
; f5y9PSIhvqGkhKLxI5RHMW7RhiwuTeWbdOjodEgYQRLUbNylP62VCLJBu56cyZx76GhlCkcCt+w2+Q
; QyRTjh6VtQ1HnI8tLBRJFLEk8iKIvr1+vZQk6l0CJZjuvr5HaiGPBqNmplf1vJXeMWhhe/szlxo1LJ
; qpJVC6x38QSu7okKsTJJxZtGNAMfcNDgo3ZUhED1GLoeiBHNonfv+UnafsMGpG7KP5EOIOE1ElCXLx
; WHZhR6BEFeSQXFASpCypxe7YIc9L3xG5dHotYeWp1/Yh5FNKABHwFBlOLIiO3KTSMXKdmvTX5s0ijk
; oHk4N8IU3Phg1i8cqVtknjtX0ISadZT62rC8kaF16FoMlkAnLkKZUciCFKqIu4xgQ9tDMvr6qaWR9C
; jvf2Pqrp7HySQQkhFZkxXBYi5FRZghwlDJCTu3MlY/oKC2f2hxDs53xEClHk1wqvkCNPSXJU2/g62m
; zKoHpPqdGaER9CsPGUySRMLpnIpgWDISaHMgBymWvWWEpvxn4IWUCvGBaFVxpoLUeOjPePjt7P6e6e
; SCotDS10kDTeyA8hx8ij/38IeVM+hJiBeeM/hFhJNtoPIZgUuw8h/wGPod0VRMxoNAAAAABJRU5Erk
; Jggg==
; thumbnail end
;
"""


def test_thumbnail_parsing() -> None:
    ast = grammar["Thumbnail"].match(thumbnail_raw)

    decoder = ThumbnailDecoder()
    image: PNGImage = decoder.visit(ast)

    h = image.header
    assert h.width == 55
    assert h.height == 40
    assert h.size == 2736

    assert isinstance(image.payload, bytes)
    with open("raw.png", "wb") as image_file:
        image_file.write(image.payload)
