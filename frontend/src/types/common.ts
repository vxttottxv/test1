// types/common.ts - ApiResponse<T>, PageResponse<T>, ApiError

export interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: 'UNAUTHORIZED' | 'FORBIDDEN' | 'NOT_FOUND' | 'INVALID_REQUEST' | 'DUPLICATE_RESOURCE' | 'SERVER_ERROR';
    message: string;
  };
}

export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}
