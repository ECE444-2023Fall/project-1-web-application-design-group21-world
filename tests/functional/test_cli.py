# def test_initialize_database(runner):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the 'flask init_db' command is called from the command line
#     THEN check the response is valid
#     """
#     output = runner.invoke(args=["init_db"])
#     assert output.exit_code == 0
#     assert "Initialized the database!" in output.output
