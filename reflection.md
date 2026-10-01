# Day 14 — Reflection

## Evaluation Report & Failure Analysis

Dùng kết quả thật trong `artifacts/benchmark_results.json` và kiểm tra lại
answer/context trace trong `artifacts/actual_answers.json` trước khi kết luận.

**Trạng thái hiện tại:** Mục 5 và câu hỏi thứ hai của Mục 7 đã trả lời xong vì
không phụ thuộc lần chạy benchmark. Mục 1–4, Mục 6 và câu hỏi đầu của Mục 7
đang để trống, chờ hai tệp artifacts — chúng chỉ được sinh ra sau khi
`.env` có khóa thật và chạy `python domain_assistant.py` rồi
`python evaluate_answers.py`. Không điền số ước đoán vào các bảng này.

---

## 1. Benchmark Results Summary

**Overall pass rate:** ____%

| Metric | Average | Min | Max | Nhận xét |
|---|---:|---:|---:|---|
| Context Recall | | | | |
| Context Precision | | | | |
| Faithfulness | | | | |
| Relevance | | | | |
| Completeness | | | | |
| Overall Score | | | | |

**Score interpretation**

- Metrics/cases ở mức Good (0.8–1.0): ____
- Metrics/cases ở mức Needs Work (0.6–0.8): ____
- Metrics/cases ở mức Significant Issues (<0.6): ____

**Failure type distribution**

| Failure Type | Count | Percentage |
|---|---:|---:|
| hallucination | | |
| irrelevant | | |
| incomplete | | |
| off_topic | | |
| refusal | | |

> *Lưu ý khi điền:* dòng `refusal` sẽ luôn bằng 0 vì chuỗi phân loại trong
> `run_full_eval()` không có nhánh nào gán nhãn đó. Đây là số 0 do cấu trúc code,
> không phải kết quả đo được — xem giải thích đầy đủ ở giới hạn 7 của Mục 7.

**Chẩn đoán tổng quan:** Vấn đề chính nằm ở retrieval, generation hay cả hai?
Dùng ít nhất hai metrics để bảo vệ kết luận.

> *Câu trả lời:*

---

## 2. Top 3 Worst Failures — 5 Whys

Phân loại failure trước khi đề xuất fix. Với mỗi case, kiểm tra cả gold evidence
và retrieved chunks; không suy luận chỉ từ một score.

### Failure 1

**ID và question:**

> *Điền:*

**Expected answer:**

> *Điền:*

**Actual answer:**

> *Điền:*

**Scores:** Context Recall: ____ | Context Precision: ____ | Faithfulness: ____ |
Relevance: ____ | Completeness: ____ | Overall: ____

**Evidence inspection:** Retriever lấy đúng/thiếu/thừa chunks nào?

> *Câu trả lời:*

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | |
| Why 1 | Tại sao symptom xảy ra? | |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | |
| Why 5 | Root cause có thể hành động được là gì? | |

**Root cause từ `find_root_cause()`:**

> *Paste output:*

**Bạn đồng ý hay không? Dẫn evidence từ trace:**

> *Câu trả lời:*

**Proposed fix cụ thể:**

> *Câu trả lời:*

### Failure 2

**ID và question:**

> *Điền:*

**Expected answer:**

> *Điền:*

**Actual answer:**

> *Điền:*

**Scores:** Context Recall: ____ | Context Precision: ____ | Faithfulness: ____ |
Relevance: ____ | Completeness: ____ | Overall: ____

**Evidence inspection:**

> *Câu trả lời:*

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | |
| Why 1 | Tại sao symptom xảy ra? | |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | |
| Why 5 | Root cause có thể hành động được là gì? | |

**Root cause và proposed fix:**

> *Câu trả lời:*

### Failure 3

**ID và question:**

> *Điền:*

**Expected answer:**

> *Điền:*

**Actual answer:**

> *Điền:*

**Scores:** Context Recall: ____ | Context Precision: ____ | Faithfulness: ____ |
Relevance: ____ | Completeness: ____ | Overall: ____

**Evidence inspection:**

> *Câu trả lời:*

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | |
| Why 1 | Tại sao symptom xảy ra? | |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | |
| Why 5 | Root cause có thể hành động được là gì? | |

**Root cause và proposed fix:**

> *Câu trả lời:*

---

## 3. Failure Clustering

Một root cause có thể tạo ra nhiều failures. Nhóm theo nguyên nhân có thể sửa,
không chỉ nhóm theo tên metric.

| Cluster | Root Cause | Failure IDs | Priority |
|---|---|---|---|
| 1 | | | High/Medium/Low |
| 2 | | | |
| 3 | | | |

**Nếu chỉ được sửa một cluster, bạn chọn cluster nào và vì sao?**

> *Câu trả lời:*

---

## 4. Improvement Log

Paste output của `generate_improvement_log()`:

```text
[paste Markdown table here]
```

**Ba improvement suggestions ưu tiên**

1. ____
2. ____
3. ____

Với mỗi suggestion, nêu metric dự kiến thay đổi và cách đo lại.

| Suggestion | Target metric | Verification method |
|---|---|---|
| | | |
| | | |
| | | |

---

## 5. Regression Testing Strategy

**Câu 1: Khi nào chạy `run_regression()` trong production workflow?**

> *Câu trả lời:*
>
> Chạy ở ba thời điểm, không phải mọi lúc.
>
> 1. **Trong kiểm thử tích hợp, trên mọi yêu cầu gộp nhánh** đụng tới ba thứ làm
>    thay đổi câu trả lời: lời nhắc hệ thống, cấu hình truy hồi (kích thước
>    chunk, `top_k`, hệ số giảm điểm khi một nguồn lặp lại, bộ xếp hạng lại), và
>    phiên bản mô hình. Tài liệu chính sách trong corpus cũng tính, vì corpus
>    đổi thì bằng chứng đổi.
> 2. **Định kỳ hằng đêm trên nhánh chính, kể cả khi không có thay đổi nào.**
>    `domain_assistant.py:260` đã đặt `temperature=0`, nên nhiễu trong cùng một
>    phiên bản là nhỏ; phần nhiễu còn lại đến từ phía nhà cung cấp — mô hình sau
>    một tên gọi có thể được cập nhật, hoặc cách gộp lô suy luận đổi. Đây là loại
>    trôi âm thầm mà chỉ lịch chạy định kỳ mới bắt được.
> 3. **Trước khi một phiên bản chính sách mới có hiệu lực.** Tài liệu OrbitTech
>    gắn `version` và `effective_date`, nên khi chính sách đổi thì chính
>    `expected_answer` cũng đổi. Lúc này phải sinh lại đường cơ sở và cho người
>    duyệt, nếu không cổng sẽ báo lùi chất lượng cho một thay đổi đúng.
>
> **Không** chạy ở móc trước mỗi lần commit: mỗi lần chạy tốn 20 lời gọi mô hình,
> quá chậm và tốn tiền cho một thao tác gõ phím. Cổng nằm ở bước gộp nhánh.
>
> Điều kiện tiên quyết mà workflow phải có: `run_regression()` cần
> `baseline_results`, nên quy trình phải lưu `artifacts/benchmark_results.json`
> theo từng thẻ phát hành, và phiên bản ứng viên luôn được so với lần phát hành
> gần nhất. Sau khi phát hành, kết quả mới trở thành đường cơ sở của vòng sau.

**Câu 2: Threshold drop 0.05 có phù hợp OrbitTech Customer Support không? Vì sao?**

> *Câu trả lời:*
>
> Không phù hợp, và lý do nằm ở số học của cỡ mẫu chứ không phải ở cảm tính.
>
> **Với 20 câu, một câu chiếm đúng 1/20 = 0.05 điểm trung bình.** Nghĩa là một
> câu rớt từ 1.0 xuống 0.0 làm trung bình giảm đúng 0.05, mà điều kiện trong
> `run_regression()` là `baseline - new > 0.05` — **nghiêm ngặt hơn**, nên một
> câu hỏng hoàn toàn vẫn lọt qua cổng. Phải tới câu thứ hai hỏng thì mức giảm
> 0.10 mới bị chặn. Với cỡ mẫu hiện tại, ngưỡng 0.05 gần như không bắt được gì
> ở mức từng câu.
>
> **Ngược lại, nó cũng quá nhạy với thay đổi vô hại.** Trung bình của 20 câu dao
> động dễ dàng vài phần trăm chỉ vì một câu trả lời đổi cách diễn đạt mà vẫn
> đúng. Kết quả là một cổng vừa bỏ sót lỗi thật vừa báo động giả — tệ hơn cả
> không có cổng, vì đội ngũ sẽ học cách bỏ qua cảnh báo.
>
> **Về mặt nghiệp vụ, mức giảm trung bình không phải là đại lượng cần bảo vệ.**
> Với trợ lý hỗ trợ khách hàng báo giá cửa sổ hoàn trả và phí nhập kho, một con
> số sai (30 ngày thay vì 21, 10% thay vì 15%) là rủi ro cam kết sai với khách
> và rủi ro tuân thủ, dù nó chỉ làm một câu trong hai mươi câu hỏng.
>
> Đề xuất cụ thể:
>
> - **Tăng cỡ mẫu lên ít nhất 50, tốt hơn là 100.** Khi đó một câu chỉ đáng
>   0.02 hoặc 0.01, và ngưỡng 0.05 mới bắt đầu có nghĩa là "nhiều câu cùng tệ
>   đi".
> - **Bổ sung cổng từng câu bên cạnh cổng trung bình:** không câu nào được đổi
>   từ đạt sang trượt; không câu Hard hay Adversarial nào được giảm quá 0.2.
>   Trung bình luôn che đúng câu quan trọng nhất.
> - **Thêm cổng số học tuyệt đối:** trích các trường nghiệp vụ (số ngày, phần
>   trăm phí, số tiền, mã phiên bản chính sách) và so khớp chính xác. Sai một
>   trường là chặn, bất kể trung bình.
> - **Lấy trung vị của ba lần lặp** khi so sánh, để một lần suy luận bất thường
>   không tự mình kích hoạt cổng.

**Câu 3: Metric/failure nào phải block deployment, metric nào chỉ alert?**

> *Câu trả lời:*
>
> **Chặn phát hành:**
>
> - **Faithfulness giảm.** Câu trả lời không trung thực với ngữ cảnh nghĩa là hệ
>   thống đang nói điều corpus không hỗ trợ. Đây là metric sinh ra cam kết sai
>   với khách hàng. Tôi áp cả hai: giảm so với đường cơ sở thì chặn, và trung
>   bình xuống dưới sàn tuyệt đối 0.75 cũng chặn.
> - **Ba câu Adversarial về phạm vi (A01–A03) trượt.** Nhóm này bảo vệ ranh giới
>   "trợ lý mô tả chính sách, không xem đơn thật". Mất ranh giới đó là mất kiểm
>   soát rủi ro, không phải mất chất lượng.
> - **Bất kỳ câu Hard hay Adversarial nào đổi từ đạt sang trượt** — chặn và chờ
>   người duyệt, không tự động cho qua.
> - **Context Recall giảm khi thay đổi nằm ở tầng truy hồi.** Nếu không truy hồi
>   được quy tắc thì faithfulness không cứu được: mô hình sẽ hoặc từ chối hoặc
>   bịa. Đây là nguyên nhân gốc của phần lớn lỗi nghiêm trọng.
>
> **Chỉ cảnh báo:**
>
> - **Relevance giảm.** Diễn đạt kém bám câu hỏi hơn là khó chịu, không phải sai
>   cam kết. Đây cũng là metric ồn nhất trong ba cái, vì trùng từ với câu hỏi
>   phụ thuộc nhiều vào cách diễn đạt.
> - **Completeness giảm.** Thiếu một ý phụ là chất lượng giảm, đưa vào danh sách
>   cải tiến. **Ngoại lệ:** nếu completeness giảm cùng lúc với một thay đổi truy
>   hồi thì phải đọc lại Context Recall trước — đó thường là triệu chứng của
>   thiếu bằng chứng, không phải của câu trả lời ngắn.
> - **Context Precision giảm.** Thứ hạng xấu đi (chunk liên quan tụt từ hạng 1
>   xuống hạng 4) gần như không đổi câu trả lời khi cả `top_k=5` chunk đều được
>   đưa vào bộ sinh. Cảnh báo và theo dõi xu hướng.
>
> **Một lỗ hổng thật trong code của chính tôi:** `run_regression()` ở
> `template.py:624` chỉ khai báo
> `metrics = ("faithfulness", "relevance", "completeness")`. Context Recall và
> Context Precision **không nằm trong cổng**, nên một thay đổi làm hỏng tầng
> truy hồi có thể đi qua cổng hồi quy mà không bị phát hiện — hai metric đó vẫn
> được tính và vẫn có trong `generate_report()`, chỉ là không được so sánh. Cách
> sửa là thêm hai tên này vào bộ `metrics`, hoặc đặt một cổng thứ hai riêng cho
> tầng truy hồi để mức chặn khác mức của tầng sinh câu trả lời.

**Câu 4: Điền evaluation stages vào flow.**

```text
Code/prompt/retrieval change
   → [Chạy benchmark trên golden dataset, ghi artifacts]
   → [So sánh với baseline: run_regression() + cổng từng câu + cổng số học]
   → [Phân tích failure và người duyệt các case Hard/Adversarial bị rớt]
   → Deploy
```

> *Giải thích:*
>
> **Giai đoạn 1 — Chạy benchmark.** Sinh `actual_answers.json` và
> `benchmark_results.json` cho phiên bản ứng viên. Bắt buộc giữ nguyên
> `temperature=0`, `top_k` và corpus so với lần chạy đường cơ sở, nếu không phần
> chênh lệch sẽ lẫn cả thay đổi không chủ đích. Vết truy hồi phải được truyền
> vào bộ đánh giá đầy đủ, vì thiếu nó thì hai metric ngữ cảnh ra `None` và giai
> đoạn 2 mất một nửa thông tin.
>
> **Giai đoạn 2 — So sánh, tự động.** `run_regression()` cho ba metric thế hệ,
> cộng hai cổng bổ sung mà một mình nó không có: cổng từng câu (không câu nào
> đạt thành trượt) và cổng số học trên các trường nghiệp vụ. Đầu ra là một giá
> trị đúng/sai để kiểm thử tích hợp chặn hoặc cho qua, kèm danh sách metric bị
> lùi để gắn vào mô tả yêu cầu gộp nhánh.
>
> **Giai đoạn 3 — Phân tích và người duyệt, không tự động.** `identify_failures()`
> lọc các câu dưới ngưỡng, `FailureAnalyzer` nhóm cụm và đề xuất nguyên nhân,
> `generate_improvement_log()` ghi lại thành bảng để theo dõi. Nhưng người thật
> phải đọc các câu Hard và Adversarial bị rớt, vì heuristic trùng từ không phát
> hiện được loại lỗi nguy hiểm nhất ở đây: trả lời đúng giọng, đúng từ vựng
> chính sách, nhưng áp dụng sai phiên bản chính sách cho sai ngày đặt hàng. Chỉ
> sau khi có quyết định của người duyệt mới sang bước phát hành.
>
> **Vòng sau khi phát hành:** giám sát truy vấn thật, chọn các truy vấn hệ thống
> trả lời kém và bổ sung chúng vào golden dataset — đó chính là Mục 6. Không có
> bước này thì benchmark chỉ đo được những gì mình đã nghĩ ra từ trước.

---

## 6. Continuous Improvement Loop

```text
Evaluate → Analyze → Improve → Augment benchmark → Repeat
```

| Priority | Action | Metric dự kiến cải thiện | Expected impact |
|---:|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

**Hai hoặc ba failure cases nào cần thêm vào benchmark ở vòng tiếp theo?**

> *Câu trả lời:*

---

## 7. Final Reflection

**Điều gì trong kết quả benchmark trái với dự đoán ban đầu của bạn?**

> *Câu trả lời:*

**Word-overlap heuristics trong lab có giới hạn gì? Nếu đưa hệ thống vào
production, bạn sẽ thay hoặc bổ sung metric nào?**

> *Câu trả lời:*
>
> **Giới hạn của heuristic trùng từ**
>
> 1. **Cả bốn metric đều là giao của hai tập hợp từ, nên chúng hoàn toàn mù với
>    trật tự từ.** `_coverage()` ở `template.py:146` tính
>    `|tokenA ∩ tokenB| / |tokenB|`. "Mức phí 10% không áp dụng cho đơn này" và
>    "Mức phí 10% áp dụng cho đơn này" cho ra hai tập từ gần như giống hệt nhau,
>    nên điểm số gần như giống hệt nhau. Phủ định, điều kiện, và phạm vi áp dụng
>    — đúng ba thứ quyết định một câu trả lời chính sách là đúng hay sai — đều
>    không đi vào phép tính.
>
> 2. **Lỗi nguy hiểm nhất của bài toán này không bị phát hiện.** Với corpus
>    OrbitTech, câu H01 hỏi một đơn đặt ngày 20/8/2026, tức thuộc phiên bản chính
>    sách 1.0 với cửa sổ 21 ngày. Một câu trả lời trích bản 2.0 vẫn chứa đầy
>    "return", "days", "opened", "restocking", "fee", nên faithfulness và
>    completeness đều cao trong khi câu trả lời sai hẳn về nghiệp vụ. Heuristic
>    không phân biệt được hai phiên bản của cùng một quy tắc.
>
> 3. **Số viết bằng chữ và số viết bằng số không trùng nhau.** `\b\w+\b` tách
>    "30-day" thành `30` và `day`, nên "30 days" và "thirty days" không có token
>    chung. Tương tự "USD 200" và "two hundred dollars". Với một corpus toàn con
>    số thời hạn và mức phí, đây là nguồn âm tính giả lớn.
>
> 4. **Câu trả lời dài được thưởng.** Faithfulness chia cho số từ của câu trả
>    lời, completeness chia cho số từ của đáp án mong đợi, và cả hai đều dùng tập
>    hợp nên lặp lại từ không bị trừ. Kết quả là một câu trả lời dài, sao chép
>    nhiều đoạn ngữ cảnh sẽ đạt faithfulness cao hơn một câu trả lời ngắn đúng
>    trọng tâm. Metric đang khuyến khích ngược điều ta muốn.
>
> 5. **Câu trả lời rỗng được faithfulness 1.0.** Luật "mẫu số rỗng thì trả 1.0"
>    trong `_coverage()` khiến một câu trả lời trống — hoặc một lời từ chối ngắn
>    — được ghi nhận là hoàn toàn trung thực với ngữ cảnh. Điểm trung bình
>    faithfulness trong báo cáo vì thế bị kéo lên một cách giả tạo.
>
> 6. **Heuristic trừng phạt lời từ chối đúng.** Ba câu A01–A03 được thiết kế để
>    trợ lý từ chối vượt phạm vi. Khi từ chối, câu trả lời không phủ các từ của
>    đáp án mong đợi nên completeness thấp, và không lặp lại từ của câu hỏi nên
>    relevance thấp — tức là hành vi đúng bị chấm là lỗi. Đây là chỗ metric và
>    mục tiêu nghiệp vụ đi ngược nhau rõ nhất.
>
> 7. **Loại lỗi `refusal` không bao giờ xuất hiện.** Chuỗi phân loại trong
>    `run_full_eval()` (`template.py:307–315`) chỉ xét faithfulness, relevance,
>    completeness và rơi vào bốn nhãn `hallucination`, `irrelevant`,
>    `incomplete`, `off_topic`. Nhãn `refusal` có trong bảng phân loại ở
>    `template.py:11` và trong bản đồ gợi ý ở `template.py:781`, nhưng không có
>    nhánh nào gán ra nó. Nên dòng `refusal` trong bảng phân bố lỗi ở Mục 1 sẽ
>    luôn bằng 0 — không phải vì hệ thống không bao giờ từ chối sai, mà vì bộ
>    phân loại không nhìn thấy loại lỗi đó.
>
> 8. **Context Precision dùng trùng từ làm định nghĩa "liên quan".** Với ngưỡng
>    0.1, một chunk chỉ cần phủ một phần mười số từ nội dung của đáp án mong đợi
>    là được coi là liên quan. Một đoạn nói chung về chính sách hoàn trả — nhiều
>    từ chung nhưng không chứa con số cần thiết — vẫn được tính, nên điểm
>    precision cao không đảm bảo chunk đó dùng được.
>
> 9. **Điểm không so sánh được giữa các câu, nên trung bình 20 câu không vững.**
>    Một đáp án mong đợi 5 từ và một đáp án 40 từ tạo ra hai thang điểm khác
>    nhau; cộng trung bình chúng lại cho ra một con số khó diễn giải. Đây chính
>    là lý do ngưỡng 0.05 ở Mục 5 Câu 2 không hoạt động như trực giác.
>
> **Nếu đưa vào production, tôi sẽ thay và bổ sung như sau**
>
> - **Trích trường nghiệp vụ rồi so khớp chính xác** — đây là thay đổi có giá
>   nhất trên mỗi đơn vị công sức. Lấy ra số ngày, phần trăm phí, số tiền, ngày
>   hiệu lực, mã phiên bản chính sách, tên tài liệu nguồn; so khớp chính xác với
>   đáp án mong đợi. Nó xử lý đúng giới hạn 1, 2, 3 và cho ra một cổng chặn phát
>   hành có ý nghĩa thật.
> - **Mô hình lớn làm giám khảo với rubric từng tiêu chí** (đã thiết kế ở
>   Exercise 3.3), thay cho trùng từ ở faithfulness và relevance. Bắt buộc kèm
>   hai điều kiện: hiệu chuẩn với nhãn của con người trên một mẫu và báo cáo hệ
>   số tương quan; và kiểm soát thiên vị vị trí bằng cách đảo thứ tự, lặp ba lần.
>   Không có hai điều kiện đó thì chỉ là thay một heuristic không đáng tin bằng
>   một heuristic đắt tiền hơn.
> - **Đánh giá faithfulness ở mức mệnh đề, không mức token.** Tách câu trả lời
>   thành từng mệnh đề nhỏ, hỏi giám khảo từng mệnh đề có được ngữ cảnh hỗ trợ
>   không. Đây là cách các thư viện đánh giá truy hồi-tăng-cường đang làm, và nó
>   khắc phục được giới hạn 4 và 5.
> - **Tương đồng ngữ nghĩa bằng vector nhúng** cho completeness, để "30 days" và
>   "thirty days", "restocking fee" và "phí nhập kho" được tính là khớp.
> - **Nhãn nhị phân riêng cho hành vi từ chối**, tách khỏi thang điểm chất lượng.
>   Mỗi câu trong bộ dữ liệu mang cờ "câu này nên từ chối hay nên trả lời", và
>   giám khảo chỉ cần xác nhận hành vi đúng loại. Không làm vậy thì ba câu
>   Adversarial về phạm vi sẽ luôn bị tính là lỗi (giới hạn 6).
> - **Mở rộng bộ phân loại lỗi để sinh được nhãn `refusal`** (giới hạn 7), nếu
>   không bảng phân bố lỗi sẽ tiếp tục che một loại lỗi có thật.
> - **Đánh giá của con người định kỳ trên mẫu nhỏ nhưng từ truy vấn thật** —
>   khoảng 30 truy vấn mỗi tuần — vừa để hiệu chuẩn giám khảo vừa làm nguồn bổ
>   sung câu mới cho bộ dữ liệu.
> - **Giám sát trực tuyến các chỉ số kết quả:** tỉ lệ người dùng hỏi lại cùng
>   một vấn đề, tỉ lệ phải chuyển sang nhân viên, tỉ lệ khiếu nại dịch vụ. Mọi
>   chỉ số ngoại tuyến đều là đại diện; những chỉ số này mới là thứ OrbitTech
>   thật sự quan tâm.
> - **Và một điểm dễ bỏ qua: chính bộ đánh giá cũng cần kiểm thử hồi quy.**
>   Giám khảo chạy bằng mô hình lớn cũng trôi theo phiên bản, nên mỗi lần đổi mô
>   hình giám khảo phải chạy lại tập hiệu chuẩn với nhãn con người đã cố định.
