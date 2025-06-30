export interface RolesResponse {
    data:        Rol[];
    total:       number;
    page:        number;
    limit:       number;
    total_pages: number;
}

export interface Rol{
    id?:         number;
    name:       string;
    created_at?: Date;
    updated_at?: Date;
    deleted_at?: Date;
    permissions?: number[];
}
