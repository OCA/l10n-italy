**Creating a Stock Closing Period**

1.  Navigate to *Inventory \> Stock Period Evaluation \> Stock Period
    Evaluation*
2.  Click **Create** to start a new closing period
3.  Configure the following fields:
    - **Reference**: Enter a unique name for this closing (e.g.,
      "2024-Q1 Closing")
    - **Close Date**: Select the date for inventory valuation
    - **Force Evaluation Method**: Choose the costing approach:
      - *Compute based on category setup*: Uses product category
        configuration
      - *Compute based on purchase average cost*: Calculates from
        purchase history
      - *Compute based on cost in product*: Uses standard product cost
      - *Compute based on FIFO*: First In, First Out valuation
      - *Compute based on LIFO (continuous)*: Last In, First Out
        valuation
    - **Last Closed** (optional): Link to previous period for
      incremental calculations
    - **Bypass Negative Quantity**: Enable to ignore products with
      negative stock

**Processing Workflow**

1.  **Start - Calculate Quantities**:
    - Click the **Start** button to begin processing
    - System calculates product quantities at the closing date
    - Review and manually adjust quantities if needed (e.g., for
      consignment stock)
    - The state changes to "In Progress"
2.  **Compute Purchase Costs**:
    - Click **Compute Purchase** to calculate product costs
    - System applies the selected evaluation method
    - For purchase average: calculates from purchase orders between
      periods
    - Process may take time for large inventories
3.  **Manual Adjustments** (if needed):
    - Edit individual line items for cost corrections
    - Modify quantities for special cases
    - Add notes or references as needed
4.  **Validation**:
    - Review the total stock amount value
    - Click **Validate** to finalize the closing
    - State changes to "Validated"
    - Period becomes read-only

**Using CSV Import**

For bulk inventory data import:

1.  Navigate to *Inventory \> Stock Period Evaluation \> Stock Period
    Import*

2.  Select the target **Stock Period Evaluation**

3.  Prepare CSV file with semicolon-separated format:

    ``` text
    CODE;COST;QTY
    PROD001;15,50;100,00
    PROD002;8,25;250,50
    PROD003;102,00;50,00
    ```

    - CODE: Product default code (must exist in system)
    - COST: Unit cost (comma or dot as decimal separator)
    - QTY: Quantity (comma or dot as decimal separator)

4.  Upload the file and click **Import**

5.  System validates products and creates closing lines

6.  The period is automatically marked as "done"

**Understanding Valuation Methods: LIFO, FIFO, and Weighted Average**

The module supports three main inventory valuation methods. Here's a practical example showing how each method calculates costs using identical transactions:

**LIFO Method (Last In, First Out)**

LIFO assumes that the most recently purchased items are sold first. This method values ending inventory using the oldest costs.

| Date       | Operation      | Qty | Balance | Unit Cost | Total Cost | Prog Cost | LIFO Avg Cost |
|------------|----------------|-----|---------|-----------|------------|-----------|---------------|
| 15/11/2023 | Purchase       | 10  | 10      | 3.00      | 30         | 30        | 3.00          |
| 15/12/2023 | Purchase       | 10  | 20      | 7.00      | 70         | 100       | 5.00          |
| 31/12/2023 | Opening Inv    | 20  | 20      | 5.00      | 100        | 100       | 5.00          |
| 31/10/2024 | Purchase       | 10  | 30      | 7.00      | 70         | 170       | 5.67          |
| 15/11/2024 | Purchase       | 10  | 40      | 10.00     | 100        | 270       | 6.75          |
| 30/11/2024 | Sale           | -10 | 30      | 10.00     | -100       | 170       | -             |
| 30/11/2024 | Sale           | -10 | 20      | 7.00      | -70        | 100       | -             |
| 30/11/2024 | Sale           | -10 | 10      | 5.00      | -50        | 50        | 5.00          |
| 02/12/2024 | Purchase       | 15  | 25      | 12.00     | 180        | 230       | 9.20          |
| 03/12/2024 | Sale           | -5  | 20      | 12.00     | -60        | 170       | 8.50          |
| 04/12/2024 | Purchase       | 10  | 30      | 15.00     | 150        | 320       | 10.67         |
| **Final**  | **Inventory**  | 30  | 30      | **15.00** | **0**      | **320**   | **10.67**     |

*Final LIFO inventory value: €320 (30 units @ €10.67 average)*

**FIFO Method (First In, First Out)**

FIFO assumes that the oldest purchased items are sold first. This method values ending inventory using the most recent costs.

| Date       | Operation      | Qty | Balance | Unit Cost | Total Cost | Prog Cost | FIFO Avg Cost |
|------------|----------------|-----|---------|-----------|------------|-----------|---------------|
| 31/12/2023 | Opening Inv    | 20  | 20      | 5.00      | 100        | 100       | 5.00          |
| 31/10/2024 | Purchase       | 10  | 30      | 7.00      | 70         | 170       | 5.67          |
| 15/11/2024 | Purchase       | 10  | 40      | 10.00     | 100        | 270       | 6.75          |
| 30/11/2024 | Sale           | -10 | 30      | 5.00      | -50        | 220       | -             |
| 30/11/2024 | Sale           | -10 | 20      | 5.00      | -50        | 170       | -             |
| 30/11/2024 | Sale           | -10 | 10      | 7.00      | -70        | 100       | 10.00         |
| 02/12/2024 | Purchase       | 15  | 25      | 12.00     | 180        | 280       | 11.20         |
| 03/12/2024 | Sale           | -5  | 20      | 10.00     | -50        | 230       | 11.50         |
| 04/12/2024 | Purchase       | 10  | 30      | 15.00     | 150        | 380       | 12.67         |
| **Final**  | **Inventory**  | 30  | 30      | **15.00** | **0**      | **380**   | **12.67**     |

*Final FIFO inventory value: €380 (30 units @ €12.67 average)*

**Weighted Average Method**

The weighted average method calculates a new average cost after each purchase, which is then applied to all units in inventory.

| Date       | Operation      | Qty | Balance | Purch Bal | Unit Cost | Total Cost | Prog Cost | Avg Cost |
|------------|----------------|-----|---------|-----------|-----------|------------|-----------|----------|
| 31/12/2023 | Opening Inv    | 20  | 20      | 20        | 5.00      | 100        | 100       | 5.00     |
| 31/10/2024 | Purchase       | 10  | 30      | 30        | 7.00      | 70         | 170       | -        |
| 15/11/2024 | Purchase       | 10  | 40      | 40        | 10.00     | 100        | 270       | 6.75     |
| 30/11/2024 | Sale           | -10 | 30      | 40        | -         | -          | 270       | -        |
| 30/11/2024 | Sale           | -10 | 20      | 40        | -         | -          | 270       | -        |
| 30/11/2024 | Sale           | -10 | 10      | 40        | -         | -          | 270       | 6.75     |
| 02/12/2024 | Purchase       | 15  | 25      | 55        | 12.00     | 180        | 450       | 8.18     |
| 03/12/2024 | Sale           | -5  | 20      | 55        | -         | -          | 450       | 8.18     |
| 04/12/2024 | Purchase       | 10  | 30      | 65        | 15.00     | 150        | 600       | 9.23     |
| **Final**  | **Inventory**  | 30  | 30      | 65        | -         | **0**      | **600**   | **9.23** |

*Final weighted average inventory value: €277 (30 units @ €9.23 average)*

**Comparison of Methods**

Using the same transaction history, the three methods produce different results:

- **LIFO**: €320 total value (€10.67/unit) - Reflects most recent purchase costs
- **FIFO**: €380 total value (€12.67/unit) - Reflects current replacement costs
- **Weighted Average**: €277 total value (€9.23/unit) - Smooths price fluctuations

**Key Observations:**

1. **LIFO** assumes newest items sold first, leaving older (cheaper) items in inventory
2. **FIFO** assumes oldest items sold first, leaving newer (more expensive) items in inventory
3. **Weighted Average** recalculates average cost after each purchase

The choice significantly impacts:
- Balance sheet inventory valuation
- Cost of goods sold (COGS) calculation
- Gross profit and taxable income
- Cash flow from operations
