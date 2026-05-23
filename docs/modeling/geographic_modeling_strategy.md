# Geographic Modeling & Distance Intelligence Design

## Objective

This document explains the final geographic modeling decisions used in the Delivery Intelligence Platform and clarifies how geographic enrichment supports logistics analytics, delivery intelligence, streaming enrichment, and seller risk investigation.

The objective of the geographic layer is not to build a geospatial mapping system, but rather to provide:

- logistics-aware analytics
- delivery distance segmentation
- seller-to-customer geographic context
- operational delivery intelligence

while preserving:

- Kimball dimensional simplicity
- warehouse performance
- analytical clarity
- dashboard usability

---

# 1. Geographic Data Understanding

During the modeling phase, a critical clarification was identified regarding the Olist geolocation dataset.

The latitude and longitude values do NOT represent:

- exact customer homes
- exact seller buildings
- physical warehouse coordinates

Instead, they represent:

# approximate Brazilian ZIP-code geographic areas

using:

# the first five digits of Brazilian postal codes.

Example from the dataset:

| ZIP Prefix | Latitude | Longitude | City      | State |
| ---------- | -------- | --------- | --------- | ----- |
| 1037       | -23.5456 | -46.6392  | sao paulo | SP    |
| 1046       | -23.5460 | -46.6448  | sao paulo | SP    |
| 1012       | -23.5477 | -46.6353  | são paulo | SP    |

This means the coordinates are:

# approximate regional enrichment data

rather than exact physical locations.

This realization directly impacted the dimensional modeling strategy.

---

# 2. Initial Architectural Consideration

Initially, the warehouse design included:

# `dim_location`

to centralize:

- ZIP codes
- latitude
- longitude
- regions
- states

The intention was to create:

# reusable geographic normalization

across:

- customers
- sellers
- future logistics marts

---

# 3. Why `dim_location` Was Rejected

After deeper analysis, the architecture intentionally removed:

# `dim_location`

because the dataset does not model location as an independent business entity.

The geographic data exists only as:

# descriptive enrichment

for:

- customers
- sellers

rather than as:

- logistics hubs
- warehouse nodes
- delivery routes
- supply-chain facilities

---

# 4. Final Geographic Modeling Decision

The final warehouse design keeps geographic attributes directly inside:

- `dim_customer`
- `dim_seller`

This follows:

# Kimball denormalized dimensional modeling principles

which prioritize:

- simpler joins
- cleaner BI models
- faster analytics
- easier dashboard development

---

# 5. Final Geographic Structure

## `dim_customer`

Contains:

| Column                   | Purpose                        |
| ------------------------ | ------------------------------ |
| customer_zip_code_prefix | Approximate customer region    |
| customer_city            | Customer city                  |
| customer_state           | Customer state                 |
| customer_region          | Macro geographic region        |
| latitude                 | Approximate customer latitude  |
| longitude                | Approximate customer longitude |

---

## `dim_seller`

Contains:

| Column                 | Purpose                      |
| ---------------------- | ---------------------------- |
| seller_zip_code_prefix | Approximate seller region    |
| seller_city            | Seller city                  |
| seller_state           | Seller state                 |
| seller_region          | Macro geographic region      |
| latitude               | Approximate seller latitude  |
| longitude              | Approximate seller longitude |

---

# 6. Why This Design Is Correct

This design is considered architecturally correct because:

| Reason                                  | Explanation                      |
| --------------------------------------- | -------------------------------- |
| No independent location business entity | Locations are descriptive only   |
| Simpler Power BI model                  | Fewer joins                      |
| Better warehouse readability            | Cleaner dimensional layer        |
| Kimball-friendly design                 | Controlled denormalization       |
| Faster analytical queries               | Less relational complexity       |
| Easier dashboard storytelling           | Direct customer/seller geography |

The architecture intentionally avoids:

# unnecessary normalization

because:
good dimensional modeling minimizes abstraction unless the abstraction creates real analytical value.

---

# 7. Distance Intelligence Strategy

Although exact logistics routing is unavailable, geographic enrichment still provides powerful analytical value.

The project therefore introduces:

# distance intelligence

through derived delivery-distance classifications.

---

# 8. `distance_bucket`

## Definition

`distance_bucket`
is a categorized approximation of seller-to-customer delivery distance.

Instead of relying only on raw GPS distances, deliveries are grouped into:

# business-friendly logistics categories

that are easier to analyze operationally.

---

# 9. Why `distance_bucket` Is Important

Distance strongly affects:

- delivery complexity
- freight cost
- shipping duration
- seller operational pressure
- delivery failure probability

The field supports important business questions such as:

- Are cross-region deliveries more likely to fail?
- Which sellers struggle with long-distance shipments?
- Does distance amplify seller overload risk?
- Which regions experience the highest logistics delays?

---

# 10. MVP Distance Classification Strategy

The initial implementation intentionally avoids complex geospatial calculations.

Instead, the project uses:

# region-based approximation logic

---

## Recommended Classification

| Condition              | distance_bucket |
| ---------------------- | --------------- |
| Same city              | Same City       |
| Same state             | Same State      |
| Same macro region      | Same Region     |
| Different macro region | Cross Region    |

This provides:

- excellent business interpretability
- low implementation complexity
- strong dashboard storytelling
- operational delivery segmentation

without requiring advanced GIS processing.

---

# 11. Advanced Geographic Enhancement (Future Phase)

The architecture remains extensible for future enhancements.

Later phases may calculate:

# approximate delivery distance in kilometers

using:

- latitude
- longitude
- Haversine distance calculations

Possible future buckets:

| Distance Range | Classification     |
| -------------- | ------------------ |
| 0–50 km        | Short Distance     |
| 51–300 km      | Medium Distance    |
| 301–1000 km    | Long Distance      |
| >1000 km       | Very Long Distance |

This enhancement is intentionally deferred because:

- the current business objectives do not require exact routing precision
- approximate regional segmentation already provides high analytical value

This represents:

# proper project scoping

rather than missing functionality.

---

# 12. Placement of Geographic Intelligence

Distance intelligence belongs inside:

# fact tables

because:
distance represents:

# contextual information about a delivery event

rather than an independent business entity.

---

## Placement in `fct_order_delivery`

| Field           | Purpose                         |
| --------------- | ------------------------------- |
| distance_bucket | Delivery logistics segmentation |

---

## Placement in `fct_seller_fulfillment`

| Field                          | Purpose                        |
| ------------------------------ | ------------------------------ |
| seller_to_customer_distance_km | Advanced operational analytics |

---

# 13. Architectural Benefits

The final geographic design provides:

| Benefit                       | Impact                         |
| ----------------------------- | ------------------------------ |
| Cleaner warehouse design      | Simpler star schema            |
| Better Power BI usability     | Fewer joins                    |
| Strong logistics storytelling | Operational insights           |
| Lower complexity              | Faster implementation          |
| Streaming enrichment support  | Seller-risk context            |
| Future extensibility          | GPS calculations later         |
| Kimball alignment             | Proper denormalized dimensions |

---

# 14. Final Architectural Decision

The final architecture intentionally:

- removes `dim_location`
- embeds geographic enrichment inside conformed dimensions
- derives distance intelligence at fact level
- prioritizes analytical simplicity over unnecessary normalization

This decision reflects:

# enterprise-grade dimensional modeling principles

where architecture is driven by:

- business value
- analytical usability
- operational clarity
- warehouse maintainability

rather than by maximizing the number of tables.
