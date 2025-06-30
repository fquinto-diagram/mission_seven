export interface PermissionsResponse {
    page?: number
    limit?: number
    total?: number
    total_pages?: number 
    data: Permission[];
}

export interface Permission {
    created_at?: Date;
    deleted_at?: null;
    name:       string;
    id?:         number|undefined;
    updated_at?: Date;
}
