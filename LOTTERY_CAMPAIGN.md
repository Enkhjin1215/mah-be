# LotteryCampaign - Ашиглах заавар

## Ерөнхий ойлголт

`LotteryCampaign` нь тодорхой хугацаанд явагдах лотерейн кампанит ажлыг илэрхийлнэ.  
Нэг Campaign дор олон `Lottery` (бүртгэл) хамаарна.

```
LotteryCampaign (2026/04/19 - 2026/05/01)
├── Lottery (утас: 99001234)
├── Lottery (утас: 88005678)
└── Lottery (утас: 77009999)
```

---

## API Endpoints

### 1. Campaign-уудын жагсаалт авах

```
GET /campaigns/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Хаврын лотерей",
    "start_date": "2026-04-19",
    "end_date": "2026-05-01",
    "is_active": true,
    "is_ongoing": true,
    "created_at": "2026-04-19T14:00:00Z",
    "updated_at": "2026-04-19T14:00:00Z"
  }
]
```

---

### 2. Шинэ Lottery бүртгэх

```
POST /lotteries/
Content-Type: multipart/form-data
```

**Дамжуулах талбарууд:**

| Талбар | Төрөл | Заавал | Тайлбар |
|--------|-------|--------|---------|
| `campaign` | integer | Үгүй | Campaign-ийн id |
| `phone_number` | string | Тийм | Утасны дугаар |
| `ebarimt_picture` | file | Тийм | Зургийн файл |
| `aimag` | string | Тийм | Аймаг/хот |
| `sum` | string | Тийм | Сум/дүүрэг |
| `horoo` | string | Тийм | Хороо |

> `lottery_number` болон `status` дамжуулах шаардлагагүй.  
> Систем автоматаар `lottery_number` үүсгэнэ (`LOT-000001` формат).  
> `status` default нь `pending`.

**Response (201 Created):**
```json
{
  "id": 1,
  "campaign": 1,
  "phone_number": "99001234",
  "lottery_number": "LOT-000001",
  "ebarimt_picture": "/media/ebarimt_pictures/photo.jpg",
  "aimag": "Улаанбаатар",
  "sum": "Баянзүрх",
  "horoo": "1-р хороо",
  "status": "pending",
  "created_at": "2026-04-21T10:00:00Z",
  "updated_at": "2026-04-21T10:00:00Z"
}
```

---

## Status утгууд

| Утга | Тайлбар |
|------|---------|
| `pending` | Хүлээгдэж байна (default) |
| `active` | Баталгаажсан |
| `rejected` | Татгалзсан |

Status-г зөвхөн admin өөрчилнө.

---

## Ердийн урсгал (Flow)

```
1. GET /campaigns/     → явагдаж байгаа campaign авна
2. POST /lotteries/    → lottery бүртгэнэ (campaign id дамжуулна)
3. Response-оос lottery_number авна
```

### Frontend жишээ (JavaScript):

```javascript
// 1. Явагдаж байгаа campaign авах
const campaigns = await fetch('/campaigns/').then(r => r.json());
const activeCampaign = campaigns.find(c => c.is_ongoing);

// 2. Lottery бүртгэх
const formData = new FormData();
formData.append('campaign', activeCampaign.id);
formData.append('phone_number', '99001234');
formData.append('ebarimt_picture', fileInput.files[0]);
formData.append('aimag', 'Улаанбаатар');
formData.append('sum', 'Баянзүрх');
formData.append('horoo', '1-р хороо');

const res = await fetch('/lotteries/', { method: 'POST', body: formData });
const data = await res.json();
console.log(data.lottery_number); // "LOT-000001"
```

---

## Admin дээр Campaign үүсгэх

1. `/admin/` → **Lottery Campaigns** → **Add**
2. Нэр, эхлэх огноо, дуусах огноо оруулна
3. `is_active` чекийг тавина
4. Хадгална

---

## Campaign-д хамаарах lottery-уудыг харах

```python
campaign = LotteryCampaign.objects.get(id=1)
lotteries = campaign.lotteries.all()
```
