# Main Flask application

from flask import Flask, render_template, request, redirect, send_from_directory, abort
import logging

# Import our custom modules
from config import config
from models.data_access import data_access, DataAccessError
from services.data_service import DataProcessor, FilterParams
from utils.helpers import setup_logging, handle_errors, get_request_params, validate_batch

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Set up logging
setup_logging(app)
logger = logging.getLogger(__name__)


@app.route("/")
def root():
    """Redirect root to main page"""
    return redirect("/hdb")


@app.route("/hdb")
@handle_errors
def index():
    """Main page showing batch selection"""
    available_batches = data_access.get_available_batches()
    return render_template("batch_select.html", batches=available_batches)


@app.route("/test-buttons")
def test_buttons():
    """Test page for debugging button functionality"""
    return render_template("test_buttons.html")


@app.route("/hdb/batch/<batch>", methods=["GET"])
@handle_errors
def batch_table(batch):
    """
    Display table for specific batch with filtering and sorting
    
    Args:
        batch: The batch year (e.g., "2024", "2023", "2022")
    """
    # Validate batch
    if not validate_batch(batch, data_access.get_available_batches()):
        logger.warning(f"Invalid batch requested: {batch}")
        abort(404)
    
    try:
        # Load data
        data = data_access.load_data(batch)
        
        # Get request parameters
        params = get_request_params()
        
        # Create filter parameters
        filter_params = FilterParams(
            search_query=params['search_query'],
            selected_branches=params['selected_branches'],
            sort_by=params['sort_by'],
            order=params['order']
        )
        
        # Process data
        processed_data = DataProcessor.process_data(data, batch, filter_params)
        
        # Get available branches for filtering
        branches = data_access.get_branches(data)
        
        # Prepare template context
        context = {
            'data': processed_data,
            'branches': branches,
            'selected_branches': filter_params.selected_branches or [],
            'sort_by': filter_params.sort_by,
            'order': filter_params.order,
            'search_query': filter_params.search_query,
            'batch': batch,
            'show_navigation': True
        }
        
        logger.info(f"Rendering table for batch {batch} with {len(processed_data)} records")
        return render_template("table.html", **context)
        
    except DataAccessError as e:
        logger.error(f"Data access error for batch {batch}: {e}")
        abort(500)
    except Exception as e:
        logger.error(f"Unexpected error processing batch {batch}: {e}")
        abort(500)


@app.route("/favicon.ico")
def favicon():
    """Serve favicon"""
    return send_from_directory('static/icons', 'favicon-32x32.png', mimetype='image/png')


@app.route("/ping")
def ping():
    """Health check endpoint"""
    return "Pong!", 200


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
