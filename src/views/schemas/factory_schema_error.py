from enum import Enum


class ErrorCode(Enum):
    MALFORMED = 1
    PHYSICIAN_NOT_FOUND = 2
    PATIENT_NOT_FOUND = 3
    METRICS_NOT_AVAILABLE = 4
    PHYSICIAN_NOT_AVAILABLE = 5
    PATIENT_NOT_AVAILABLE = 6


error_mapping = {
    ErrorCode.MALFORMED.value: "malformed request",
    ErrorCode.PHYSICIAN_NOT_FOUND.value: "physician not found",
    ErrorCode.PATIENT_NOT_FOUND.value: "patient not found",
    ErrorCode.METRICS_NOT_AVAILABLE.value: "metrics service not available",
    ErrorCode.PHYSICIAN_NOT_AVAILABLE.value: "physicians service not available",
    ErrorCode.PATIENT_NOT_AVAILABLE.value: "patients service not available"
}


def create_schema_error(error_code):
    json = {
        "error": {
            "message": error_mapping[error_code],
            "code": error_code
        }
    }
    return json
