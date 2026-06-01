# Seller Acquisition Domain Analytical Validation Report

## Project

Olist Seller Intelligence Platform

## Document Type

Analytical Validation & Business Justification Report

## Objective

The purpose of this analysis was to determine whether the Olist marketing acquisition dataset contributes meaningful business value to the enterprise data warehouse and whether it justifies implementation of a dedicated acquisition-focused Gold Data Mart.

Unlike traditional marketplace analyses that begin at the order level, this project aims to model the complete seller lifecycle:

Seller Acquisition
→ Seller Operations
→ Delivery Performance
→ Customer Satisfaction
→ Revenue Impact

The acquisition domain was evaluated to determine whether upstream marketing and seller onboarding characteristics influence downstream operational and customer outcomes.

---

# 1. Dataset Validation

## Marketing Funnel Dataset

The marketing dataset contains approximately 8,000 Marketing Qualified Leads (MQLs) generated between June 2017 and May 2018.

### Funnel Metrics

| Metric          | Value  |
| --------------- | ------ |
| Total MQLs      | 8,000  |
| Closed Deals    | 842    |
| Conversion Rate | 10.53% |

### Interpretation

Approximately one out of every ten qualified leads successfully converted into an onboarded seller.

This confirms that the acquisition dataset represents a meaningful commercial funnel rather than a simple lead registry.

---

# 2. Temporal Coverage Validation

## Marketplace Activity

| Metric       | Date Range          |
| ------------ | ------------------- |
| Orders       | Sep 2016 – Oct 2018 |
| MQLs         | Jun 2017 – May 2018 |
| Closed Deals | Dec 2017 – Nov 2018 |

### Finding

A significant overlap exists between acquisition activity and marketplace operations.

This overlap allows seller acquisition behavior to be connected to:

- Seller performance
- Order fulfillment
- Delivery outcomes
- Customer reviews

### Result

PASS

The acquisition dataset is temporally compatible with the operational Olist ecosystem.

---

# 3. Seller Coverage Validation

## Coverage Analysis

| Metric                   | Value |
| ------------------------ | ----- |
| Total Sellers            | 3,095 |
| Sellers Linked to Funnel | 842   |
| Coverage Percentage      | 27.2% |

### Interpretation

More than one quarter of all marketplace sellers can be linked to a documented acquisition journey.

This level of coverage is substantial enough to support strategic seller lifecycle analytics.

### Result

PASS

The acquisition dataset has sufficient marketplace representation.

---

# 4. Acquisition Source Analysis

## Lead Distribution

| Acquisition Source | Leads |
| ------------------ | ----- |
| Organic Search     | 2,296 |
| Paid Search        | 1,586 |
| Social             | 1,350 |
| Unknown            | 1,099 |
| Direct Traffic     | 499   |
| Email              | 493   |
| Referral           | 284   |

### Key Finding

The acquisition funnel is highly concentrated.

Organic Search, Paid Search, and Social channels account for approximately 65% of all incoming leads.

### Business Implication

Marketing investment and seller recruitment strategies are heavily dependent on a small number of acquisition channels.

---

# 5. Funnel Conversion Analysis

## Converted Sellers by Source

| Source         | Converted Sellers |
| -------------- | ----------------- |
| Organic Search | 271               |
| Paid Search    | 195               |
| Unknown        | 179               |
| Social         | 75                |

### Key Finding

Lead volume does not necessarily translate into seller conversion.

Social media generated a large number of leads but produced significantly fewer converted sellers compared to Organic Search and Paid Search.

### Business Implication

Marketing efficiency should be evaluated using conversion quality rather than lead volume alone.

---

# 6. Acquisition → Seller Performance Validation

## Objective

Determine whether acquisition channels produce sellers with different operational characteristics.

### Metrics Evaluated

- Seller Monthly Orders
- Workload Classification
- Seller Operational Volume

### Results

| Source         | Avg Monthly Orders |
| -------------- | ------------------ |
| Paid Search    | 26.35              |
| Organic Search | 12.86              |
| Social         | 12.99              |
| Direct Traffic | 4.21               |
| Referral       | 4.30               |

### Key Findings

Paid Search sellers generate significantly higher operational volume than Organic Search sellers.

Organic Search and Social sellers exhibit similar operational productivity despite substantial differences in lead volume and conversion efficiency.

### Result

PASS

Acquisition source influences seller operational behavior.

---

# 7. Acquisition → Delivery Performance Validation

## Objective

Determine whether acquisition channels produce different delivery outcomes.

### Metrics Evaluated

- On-Time Delivery Rate
- Delivery Delay
- Delivery Status Distribution
- Geographic Shipping Complexity

### Results

| Source         | On-Time Delivery Rate |
| -------------- | --------------------- |
| Organic Search | 95.48%                |
| Social         | 94.09%                |
| Paid Search    | 93.71%                |
| Direct Traffic | 92.71%                |
| Unknown        | 90.80%                |

### Key Findings

Organic Search sellers demonstrate the strongest delivery reliability among major acquisition channels.

Paid Search sellers generate higher operational volume but slightly lower delivery performance.

Unknown attribution sellers consistently underperform.

### Result

PASS

Acquisition source influences delivery outcomes.

---

# 8. Acquisition → Customer Satisfaction Validation

## Objective

Determine whether acquisition channels influence customer experience.

### Metrics Evaluated

- Average Review Score
- Positive Review Rate
- Negative Review Rate
- Delivery Complaint Rate
- Sentiment Distribution

### Results

| Source         | Avg Review Score | Negative Reviews |
| -------------- | ---------------- | ---------------- |
| Organic Search | 4.39             | 8.83%            |
| Paid Search    | 4.32             | 10.31%           |
| Social         | 4.28             | 10.80%           |
| Unknown        | 4.17             | 13.58%           |

### Delivery Complaint Rate

| Source         | Complaint Rate |
| -------------- | -------------- |
| Organic Search | 1.43%          |
| Paid Search    | 2.86%          |
| Social         | 3.34%          |
| Unknown        | 5.35%          |

### Key Findings

Organic Search sellers consistently achieve:

- Highest customer satisfaction
- Lowest complaint rates
- Lowest negative review percentages

Unknown attribution sellers consistently produce weaker customer outcomes.

### Result

PASS

Acquisition source influences customer satisfaction.

---

# 9. Business Storytelling Validation

The acquisition analysis successfully validated the project's core analytical narrative:

Acquisition Source
↓
Seller Quality
↓
Operational Performance
↓
Delivery Reliability
↓
Customer Satisfaction

This demonstrates that acquisition is not merely a marketing attribute.

Instead, acquisition source acts as an upstream business driver that influences downstream marketplace outcomes.

---

# 10. Gold Layer Justification

## Why fct_seller_acquisition Should Exist

The analysis demonstrates that acquisition characteristics influence:

- Seller productivity
- Operational workload
- Delivery reliability
- Customer satisfaction

These relationships cannot be fully explained using operational marketplace data alone.

A dedicated acquisition mart enables analysis of:

- Channel effectiveness
- Seller quality by source
- Conversion performance
- Lifecycle seller value
- Acquisition ROI

### Recommendation

Implement:

fct_seller_acquisition

as a dedicated Gold Fact Table.

---

# 11. Power BI Storytelling Opportunities

The acquisition mart enables executive-level dashboards such as:

## Acquisition Overview

- Lead Funnel
- Conversion Funnel
- Channel Effectiveness

## Seller Quality Dashboard

- Seller Volume by Source
- Seller Performance by Source
- High Value Seller Analysis

## Delivery Intelligence Dashboard

- On-Time Rate by Source
- Delivery Complaint Rate by Source
- Late Delivery Analysis

## Customer Satisfaction Dashboard

- Review Scores by Source
- Sentiment Distribution
- Complaint Analysis

## Seller Lifecycle Dashboard

Acquisition
→ Seller Performance
→ Delivery Performance
→ Customer Satisfaction

This dashboard becomes the centerpiece of the platform narrative.

---

# 12. Future Streaming & Real-Time Value

The acquisition domain provides strong foundations for future streaming architectures.

Potential real-time use cases include:

## Real-Time Lead Monitoring

Track incoming leads by channel.

## Conversion Monitoring

Monitor conversion rates continuously.

## Seller Quality Prediction

Predict seller operational performance based on acquisition characteristics.

## Delivery Risk Prediction

Identify sellers likely to experience delivery failures.

## Customer Satisfaction Prediction

Estimate future review performance using acquisition and operational signals.

## Acquisition Channel Alerting

Detect underperforming acquisition channels in near real time.

These use cases align naturally with Kafka-based event-driven architectures and future real-time marketplace intelligence platforms.

---

# Final Conclusion

The seller acquisition dataset was successfully validated as a strategic analytical domain.

Evidence demonstrates measurable relationships between acquisition source, seller operational performance, delivery outcomes, and customer satisfaction.

The acquisition domain extends the project beyond traditional e-commerce reporting by enabling end-to-end seller lifecycle intelligence.

Final Recommendation:

Proceed with implementation of:

fct_seller_acquisition

as a core Gold Layer fact table and include acquisition intelligence as a primary storytelling component throughout the warehouse, dashboards, and future streaming architecture.
