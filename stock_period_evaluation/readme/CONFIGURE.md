**User Access Configuration**

1.  **Security Groups**:

    - **Stock Period Evaluation Manager**
      (`stock_period_evaluation.group_stock_period_evaluation_manager`):
      - Full access to create, edit, validate, and delete closing
        periods
      - Access to import wizard and all reporting functions
      - Can force evaluation methods for cost calculation
    - **Stock Period Evaluation User Read Only**
      (`stock_period_evaluation.group_stock_period_evaluation_user_readonly`):
      - View-only access to closing periods and reports
      - Cannot modify or create new periods

2.  **User Assignment**:

    Go to *Settings \> Users & Companies \> Users*:

    - Select the user to configure
    - Assign appropriate Stock Period Evaluation group

**System Parameters**

The module uses a system parameter for default configuration:

- **Default Last Close Date**: `stock_period_evaluation.last_close_date`
  - Default value: 2010-01-01
  - Can be modified via *Settings \> Technical \> System Parameters*
  - Used when no previous closing period is selected

**Performance Settings**

Consider these optional configurations for large databases:

- **Bypass Negative Quantities**: Enable to skip products with negative
  stock during calculations
- **No Recompute Lines**: Skip recalculation of quantities for existing
  lines to improve performance
