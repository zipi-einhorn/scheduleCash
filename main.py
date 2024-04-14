import os

from flask import Flask, jsonify, request

from flasgger import Swagger
from extractorTransformerLoader import extract_sailing_schedules, transform_schedules, load_to_csv, load_to_csv_exist

app = Flask(__name__)
Swagger(app)


@app.route('/schedule_cache', methods=['GET'])
def schedule_cache():
    """
    Run schedule cache.
    ---
    parameters:
      - name: carrier_id
        in: query
        type: integer
        required: true
        description: ID of the carrier.
      - name: page
        in: query
        type: integer
        default: 1
        required: true
        description: Page number.
      - name: page_size
        in: query
        type: integer
        default: 20
        required: true
        description: Page size.
    responses:
      200:
        description: Extraction complete.
      400:
        description: Bad request.
      500:
        description: Internal server error.
    """
    # Get query parameters
    carrier_id = request.args.get('carrier_id')
    page = request.args.get('page')
    page_size = request.args.get('page_size')

    # Validate parameters
    if carrier_id is None or page is None:
        return jsonify({'error': 'Missing parameters: carrier_id are required.'}), 400

    # Convert page to integer
    try:
        page = int(page)
    except ValueError:
        return jsonify({'error': 'Invalid page value. Page must be an integer.'}), 400

    # Run extraction process
    try:
        extracted_data = extract_sailing_schedules(carrier_id)
        transformed_data = transform_schedules(extracted_data, page, page_size)
        file_path = os.path.join("schedulesCache/", f"{carrier_id}_SchedulesCache.csv")
        if os.path.exists(file_path):
            load_to_csv_exist(carrier_id, transformed_data)
        else:
            load_to_csv(carrier_id, transformed_data)
        return jsonify({'status': 'Extraction complete'})
    except Exception as e:
        return jsonify({'error': f'An error occurred during extraction: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
