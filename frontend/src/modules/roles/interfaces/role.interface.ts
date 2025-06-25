export interface RolesResponse {
    data:        Role[];
    total:       number;
    page:        number;
    limit:       number;
    total_pages: number;
}

export interface Role {
    id:         number;
    name:       string;
    created_at?: Date;
    updated_at?: Date;
    deleted_at?: Date;
}
