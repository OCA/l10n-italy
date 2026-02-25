**18.0.1.1.0 (2024-09-26)**

- **New Features**:
  - Added FIFO (First In, First Out) valuation method
  - Added LIFO (Last In, First Out) continuous valuation method
  - Integrated evaluation details field showing transaction-level cost
    breakdown
  - Added formatted value display for evaluation details
- **Technical Improvements**:
  - Ported FIFO/LIFO functionality from
    stock_close_period_evaluation_method module
  - Enhanced \_evaluate_product() method to support new valuation
    methods
  - Added price_calculation() method for FIFO/LIFO computation
  - Implemented \_get_tuples() for transaction processing
  - Added update_tuple() static method for valuation type handling
  - Included \_fix_zero_values() for handling missing prices
- **UI Enhancements**:
  - Added evaluation_details field to tree and form views
  - Made evaluation details optional/hidden in tree view for better
    performance
  - Displayed detailed cost breakdown in form view

**18.0.1.0.0**

- Initial release for Odoo 18
- Stock period evaluation with average and standard cost methods
- Multi-location and multi-company support
- Excel export functionality
- CSV import capabilities
