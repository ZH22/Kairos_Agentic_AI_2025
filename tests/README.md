# Tests Directory

## Structure

### `/unit/`
Unit tests for individual components and functions:
- `test_db_handler.py` - Database operations testing
- `test_db_filter.py` - Database filtering functionality
- `test_query_validation.py` - Query validation logic
- `test_improved_validation.py` - Enhanced validation testing

### `/integration/`
Integration tests for complete workflows:
- `test_buyer_*.py` - Buyer workflow testing
- `test_browse_*.py` - Browse functionality testing

### `/fixtures/`
Test data and fixtures for consistent testing

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run integration tests only
python -m pytest tests/integration/

# Run specific test file
python -m pytest tests/unit/test_db_handler.py
```

## Test Categories

- **Unit Tests**: Fast, isolated tests for individual functions
- **Integration Tests**: Slower tests that verify component interactions
- **Fixtures**: Reusable test data and mock objects