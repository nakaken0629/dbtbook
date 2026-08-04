#!/usr/bin/env python3
"""
オンラインペットショップ サンプルデータ生成スクリプト
sources/masters にマスタCSVを、
sources/transactions（customer.csv, sales/, sales_detail/）にトランザクションCSVを出力する。
"""
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(42)
# created_at/updated_at 専用の乱数系列。
# 既存カラム（sales_id, customer_id, 商品選択, quantity等）の乱数系列に
# 影響を与えないよう、random モジュールの共有状態とは分離する。
ts_rng = random.Random(20260701)

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / "sources"
MASTERS_DIR = SOURCES_DIR / "masters"
TRANSACTIONS_DIR = SOURCES_DIR / "transactions"
SALES_DIR = TRANSACTIONS_DIR / "sales"
SALES_DETAIL_DIR = TRANSACTIONS_DIR / "sales_detail"

for d in (MASTERS_DIR, TRANSACTIONS_DIR, SALES_DIR, SALES_DETAIL_DIR):
    d.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list, rows: list):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def random_date_between(start_date: date, end_date: date) -> date:
    days_span = (end_date - start_date).days
    return start_date + timedelta(days=ts_rng.randint(0, days_span))


def gen_timestamps(base_date: date, max_update_days: int = 7):
    """base_date 当日のランダムな時刻を created_at、
    その後 0〜max_update_days 日以内のランダムな時刻を updated_at として返す。"""
    created_at = datetime.combine(base_date, datetime.min.time()) + timedelta(
        seconds=ts_rng.randint(0, 24 * 3600 - 1)
    )
    updated_at = created_at + timedelta(seconds=ts_rng.randint(0, max_update_days * 24 * 3600))
    return created_at.isoformat(sep=" "), updated_at.isoformat(sep=" ")


# マスタ系（species_master, goods_category_master, product_master）は
# 販売開始（2026-07-01）より前のこの期間中にセットアップされた想定
MASTER_SETUP_START = date(2026, 6, 1)
MASTER_SETUP_END = date(2026, 6, 30)

# ---------- species_master ----------
SPECIES = [
    (1, "犬"),
    (2, "猫"),
    (3, "鳥"),
    (4, "魚"),
    (5, "爬虫類"),
]
write_csv(
    MASTERS_DIR / "species_master.csv",
    ["species_id", "species_name", "created_at", "updated_at"],
    [
        (*s, *gen_timestamps(random_date_between(MASTER_SETUP_START, MASTER_SETUP_END)))
        for s in SPECIES
    ],
)

# ---------- goods_category_master ----------
GOODS_CATEGORIES = [
    (1, "えさ"),
    (2, "すみか"),
    (3, "遊び道具"),
]
write_csv(
    MASTERS_DIR / "goods_category_master.csv",
    ["goods_category_id", "goods_category_name", "created_at", "updated_at"],
    [
        (*g, *gen_timestamps(random_date_between(MASTER_SETUP_START, MASTER_SETUP_END)))
        for g in GOODS_CATEGORIES
    ],
)

# ---------- product_master (PET) ----------
# (product_id, species_id, breed_name, description, price)
PETS = [
    (1, 1, "ブルドッグ", "がっしりした体格で人懐っこい犬種", 280000),
    (2, 1, "チワワ", "小型で活発、室内飼いに人気の犬種", 220000),
    (3, 1, "柴犬", "日本原産の代表的な犬種", 180000),
    (4, 2, "マンチカン", "短い脚が特徴の人気猫種", 200000),
    (5, 2, "スコティッシュフォールド", "折れ耳が特徴のおっとりした猫種", 190000),
    (6, 2, "アメリカンショートヘア", "丈夫で穏やかな性格の猫種", 150000),
    (7, 3, "セキセイインコ", "カラフルで人に慣れやすい小型インコ", 8000),
    (8, 3, "オカメインコ", "冠羽が特徴の人懐っこいインコ", 15000),
    (9, 3, "ジュウシマツ", "飼育しやすい小型の鳴き鳥", 5000),
    (10, 4, "メダカ", "丈夫で飼育しやすい淡水魚", 200),
    (11, 4, "グッピー", "カラフルな尾びれが特徴の熱帯魚", 500),
    (12, 4, "ネオンテトラ", "群泳が美しい小型熱帯魚", 300),
    (13, 5, "フトアゴヒゲトカゲ", "温和な性格で人気の爬虫類", 45000),
    (14, 5, "ヒョウモントカゲモドキ", "飼育しやすい人気のヤモリ", 35000),
    (15, 5, "ミシシッピアカミミガメ", "丈夫で長寿命の水棲ガメ", 3000),
]

# ---------- product_master (GOODS) ----------
# (product_id, goods_category_id, species_id, goods_name, price)
GOODS = [
    (16, 1, 1, "ドッグフード(成犬用)", 3500),
    (17, 2, 1, "犬用ケージ", 12000),
    (18, 3, 1, "犬用ボール", 800),
    (19, 1, 2, "キャットフード", 2800),
    (20, 2, 2, "猫用キャットタワー", 15000),
    (21, 3, 2, "猫じゃらし", 600),
    (22, 1, 3, "小鳥用シード", 900),
    (23, 2, 3, "鳥かご", 8000),
    (24, 3, 3, "バードトーイ", 700),
    (25, 1, 4, "熱帯魚用フレークフード", 500),
    (26, 2, 4, "水槽セット", 6000),
    (27, 3, 4, "水草オーナメント", 1200),
    (28, 1, 5, "爬虫類用人工飼料", 1500),
    (29, 2, 5, "爬虫類用ケージ", 20000),
    (30, 3, 5, "シェルター(隠れ家)", 2500),
]

# ---------- product_master (ペット・グッズを統合) ----------
# species_id は両タイプ共通の属性（ペット=動物種そのもの、グッズ=対象動物種）。
# goods_category_id は GOODS のみ、description は PET のみ値を持ち、他方は空欄(NULL)。
product_master_rows = [
    (p[0], "PET", p[2], p[4], True, p[1], "", p[3]) for p in PETS
]
product_master_rows += [
    (g[0], "GOODS", g[3], g[4], True, g[2], g[1], "") for g in GOODS
]
product_master_rows.sort(key=lambda r: r[0])

write_csv(
    MASTERS_DIR / "product_master.csv",
    ["product_id", "product_type", "product_name", "price", "is_active",
     "species_id", "goods_category_id", "description", "created_at", "updated_at"],
    [
        (*row, *gen_timestamps(random_date_between(MASTER_SETUP_START, MASTER_SETUP_END), max_update_days=20))
        for row in product_master_rows
    ],
)

PRODUCT_PRICE = {row[0]: row[3] for row in product_master_rows}
PET_IDS = [p[0] for p in PETS]
GOODS_IDS = [g[0] for g in GOODS]

# ---------- customer（マスタではなくトランザクション系として transactions/ に置く） ----------
# customer レコードの created_at はこの期間内に収まる想定（registered_at とは独立）
CUSTOMER_CREATED_AT_START = date(2026, 4, 1)
CUSTOMER_CREATED_AT_END = date(2026, 6, 30)

CUSTOMERS = [
    (1, "田中太郎", "tanaka.taro@example.com", "東京都新宿区"),
    (2, "佐藤花子", "sato.hanako@example.com", "大阪府大阪市"),
    (3, "鈴木一郎", "suzuki.ichiro@example.com", "神奈川県横浜市"),
    (4, "高橋美咲", "takahashi.misaki@example.com", "愛知県名古屋市"),
    (5, "伊藤健太", "ito.kenta@example.com", "福岡県福岡市"),
    (6, "渡辺さくら", "watanabe.sakura@example.com", "北海道札幌市"),
    (7, "山本大輔", "yamamoto.daisuke@example.com", "埼玉県さいたま市"),
    (8, "中村結衣", "nakamura.yui@example.com", "千葉県千葉市"),
    (9, "小林翔太", "kobayashi.shota@example.com", "兵庫県神戸市"),
    (10, "加藤凛", "kato.rin@example.com", "京都府京都市"),
    (11, "吉田健二", "yoshida.kenji@example.com", "静岡県静岡市"),
    (12, "山田美緒", "yamada.mio@example.com", "広島県広島市"),
    (13, "佐々木大和", "sasaki.yamato@example.com", "宮城県仙台市"),
    (14, "松本ゆな", "matsumoto.yuna@example.com", "新潟県新潟市"),
    (15, "井上健一", "inoue.kenichi@example.com", "岡山県岡山市"),
]

customer_rows = []
for c in CUSTOMERS:
    # registered_at は created_at と同じ値にする
    created_at, updated_at = gen_timestamps(
        random_date_between(CUSTOMER_CREATED_AT_START, CUSTOMER_CREATED_AT_END), max_update_days=180
    )
    customer_rows.append((*c, created_at, created_at, updated_at))

write_csv(
    TRANSACTIONS_DIR / "customer.csv",
    ["customer_id", "customer_name", "email", "address", "registered_at", "created_at", "updated_at"],
    customer_rows,
)
CUSTOMER_IDS = [c[0] for c in CUSTOMERS]

# ---------- sales / sales_detail (2026-07-01 〜 2026-07-31, 日次ファイル) ----------
START_DATE = date(2026, 7, 1)
END_DATE = date(2026, 7, 31)

sales_id_seq = 1
detail_id_seq = 1
total_orders = 0
total_details = 0

current = START_DATE
while current <= END_DATE:
    day_sales_rows = []
    day_detail_rows = []

    num_orders = random.randint(3, 8)
    for _ in range(num_orders):
        sales_id = sales_id_seq
        sales_id_seq += 1
        customer_id = random.choice(CUSTOMER_IDS)

        num_items = random.randint(1, 3)
        chosen_products = random.sample(PET_IDS + GOODS_IDS, k=num_items)

        total_amount = 0
        order_detail_rows = []
        for product_id in chosen_products:
            quantity = 1 if product_id in PET_IDS else random.randint(1, 3)
            unit_price = PRODUCT_PRICE[product_id]
            amount = unit_price * quantity
            total_amount += amount

            order_detail_rows.append((detail_id_seq, sales_id, product_id, quantity, unit_price, amount))
            detail_id_seq += 1

        # 受注日時（order_date 当日のランダムな時刻）と更新日時（作成後0〜180分後）
        order_created_at = datetime.combine(current, datetime.min.time()) + timedelta(
            seconds=ts_rng.randint(0, 24 * 3600 - 1)
        )
        order_updated_at = order_created_at + timedelta(minutes=ts_rng.randint(0, 180))

        day_sales_rows.append(
            (
                sales_id, customer_id, current.isoformat(), total_amount,
                order_created_at.isoformat(sep=" "), order_updated_at.isoformat(sep=" "),
            )
        )

        for detail_id, s_id, product_id, quantity, unit_price, amount in order_detail_rows:
            # 明細は受注と同時に作成され、0〜60分後に更新されることがある想定
            detail_created_at = order_created_at
            detail_updated_at = detail_created_at + timedelta(minutes=ts_rng.randint(0, 60))
            day_detail_rows.append(
                (
                    detail_id, s_id, product_id, quantity, unit_price, amount,
                    detail_created_at.isoformat(sep=" "), detail_updated_at.isoformat(sep=" "),
                )
            )

    date_str = current.strftime("%Y%m%d")
    write_csv(
        SALES_DIR / f"sales_{date_str}.csv",
        ["sales_id", "customer_id", "order_date", "total_amount", "created_at", "updated_at"],
        day_sales_rows,
    )
    write_csv(
        SALES_DETAIL_DIR / f"sales_detail_{date_str}.csv",
        ["sales_detail_id", "sales_id", "product_id", "quantity", "unit_price", "amount", "created_at", "updated_at"],
        day_detail_rows,
    )

    total_orders += len(day_sales_rows)
    total_details += len(day_detail_rows)
    current += timedelta(days=1)

print(f"products: {len(product_master_rows)}, customers: {len(CUSTOMERS)}, orders: {total_orders}, detail rows: {total_details}")
