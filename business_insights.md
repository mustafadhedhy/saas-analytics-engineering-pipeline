# Business Insights

This project analyzes synthetic SaaS product, revenue, customer, and support data using a modern analytics engineering workflow.

## Executive Summary

The final analytics layer combines account, user, product usage, subscription, and support ticket data into dashboard-ready marts. The Power BI Executive Summary dashboard gives business users a high-level view of customer activity, recurring revenue, product engagement, and account health.

## Key Metrics

The dashboard tracks:

- Total accounts
- Total users
- Active users
- Active monthly recurring revenue
- Total product events
- Open support tickets
- Account health status
- Revenue by plan type
- Accounts by country

## Account Health Logic

Account health is calculated using product usage, revenue, and support activity.

Accounts are classified as:

- Healthy: strong recent activity, paid revenue, and low open support burden
- Monitor: moderate product activity or active revenue
- At Risk: low recent activity and weaker engagement indicators

This allows customer success and leadership teams to quickly identify which accounts may need attention.

## Revenue Insights

The revenue mart summarizes active MRR by plan type. This helps identify which customer segments contribute the most recurring revenue and how revenue is distributed across Free, Starter, Professional, and Enterprise plans.

## Product Usage Insights

The product usage marts track events such as logins, dashboard views, AI feature usage, report exports, file uploads, project creation, and support page views. These metrics help product teams understand feature adoption and engagement trends.

## Support Insights

The support mart tracks ticket volume, open tickets, priority, category, and resolution hours. This supports analysis of customer support load and service performance.

## Business Value

This project demonstrates how raw operational data can be transformed into clean, tested, and business-ready analytics tables. The final dashboard can support decisions around customer success, product adoption, revenue monitoring, and operational support.