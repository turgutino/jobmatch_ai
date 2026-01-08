import contextlib
import io

def run_python_code(code: str):
    """
    Executes user-provided Python code safely and returns output or errors.
    """

    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})
        return {
            "success": True,
            "output": output_buffer.getvalue()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
