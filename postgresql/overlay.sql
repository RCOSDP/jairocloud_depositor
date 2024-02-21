
-- 新テーブルの作成 (affiliation_id)
create table public.affiliation_id (
  created timestamp(6) without time zone not null
  , updated timestamp(6) without time zone not null
  , id integer not null
  , affiliation_idp_url character varying(80) not null
  , affiliation_name character varying(80) not null
);

-- 主キーの作成
alter table public.affiliation_id add constraint pk_affiliation_id primary key (id);

-- インデックスとユニーク制約の作成
create unique index uq_affiliation_idp_url on public.affiliation_id(affiliation_idp_url);
create index ix_affiliation_name on public.affiliation_id(affiliation_name);

-- 制約の作成
alter table public.affiliation_id add constraint "id_not_null" check (id IS NOT NULL);
alter table public.affiliation_id add constraint "affiliation_idp_url_not_null" check (affiliation_idp_url IS NOT NULL);
alter table public.affiliation_id add constraint "affiliation_name_not_null" check (affiliation_name IS NOT NULL);

-- シークエンス
create sequence public.affiliation_id_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

alter sequence public.affiliation_id_id_seq owned by public.affiliation_id.id;

-- 「default」レコードの追加
insert into affiliation_id(created,updated,id,affiliation_idp_url,affiliation_name)
values(CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,1,'-','default');


-- 新テーブルの作成 (user)
create table public.user (
  created timestamp(6) without time zone not null
  , updated timestamp(6) without time zone not null
  , id integer not null
  , user_id character varying(80) not null
  , affiliation_id integer not null
  , user_orcid character varying(80)
  , role character varying(80)
);

-- 主キーの作成
alter table public.user add constraint pk_user primary key (id);

-- インデックスとユニーク制約の作成
create index ix_user_id on public.user(user_id);
create index ix_user_orcid on public.user(user_orcid);
create index ix_role on public.user(role);

-- 制約の作成
alter table public.user add constraint "id_not_null" check (id IS NOT NULL);
alter table public.user add constraint "user_id_not_null" check (user_id IS NOT NULL);
alter table public.user add constraint "affiliation_id_not_null" check (affiliation_id IS NOT NULL);

-- シークエンス
create sequence public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
    
alter sequence public.user_id_seq owned by public.user.id;

-- 外部キー情報追加
alter table public.user
  add constraint fk_user_affiliation_id_affiliation_id  foreign key (affiliation_id)
  references public.affiliation_id(id);


-- 新テーブルの作成(affiliation_repository)
create table public.affiliation_repository (
  created timestamp(6) without time zone not null
  , updated timestamp(6) without time zone not null
  , id integer not null
  , affiliation_id integer not null
  , repository_url character varying(80) not null
  , access_token character varying(80) not null
);

-- 主キーの作成
alter table public.affiliation_repository  add constraint pk_affiliation_repository primary key (id);

-- インデックスとユニーク制約の作成
create index ix_repository_url on public.affiliation_repository(repository_url);
create index ix_access_token on public.affiliation_repository(access_token);

-- 制約の作成
alter table public.affiliation_repository add constraint "id_not_null" check (id IS NOT NULL);
alter table public.affiliation_repository add constraint "affiliation_id_not_null" check (affiliation_id IS NOT NULL);
alter table public.affiliation_repository add constraint "repository_url_not_null" check (repository_url IS NOT NULL);
alter table public.affiliation_repository add constraint "access_token_not_null" check (access_token IS NOT NULL);

-- シークエンス
create sequence public.affiliation_repository_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
    
alter sequence public.affiliation_repository_id_seq owned by public.affiliation_repository.id;

alter table public.user
  add constraint fk_affiliation_repository_affiliation_id_affiliation_id  foreign key (affiliation_id)
  references public.affiliation_id(id);
