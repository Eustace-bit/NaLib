--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0 (Debian 13.0-4)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1+b1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO angledimensions;

--
-- Name: borrowedbooks; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.borrowedbooks (
    "borrowId" character varying NOT NULL,
    "resourceId" character varying,
    "borrowedBy" character varying,
    "borrowedDate" character varying,
    "returnDate" character varying
);


ALTER TABLE public.borrowedbooks OWNER TO angledimensions;

--
-- Name: lendingbehavior; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.lendingbehavior (
    "behaviorID" integer NOT NULL,
    "membershipID" character varying NOT NULL,
    "overdueCount" integer,
    preference character varying
);


ALTER TABLE public.lendingbehavior OWNER TO angledimensions;

--
-- Name: lendingbehavior_behaviorID_seq; Type: SEQUENCE; Schema: public; Owner: angledimensions
--

CREATE SEQUENCE public."lendingbehavior_behaviorID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."lendingbehavior_behaviorID_seq" OWNER TO angledimensions;

--
-- Name: lendingbehavior_behaviorID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: angledimensions
--

ALTER SEQUENCE public."lendingbehavior_behaviorID_seq" OWNED BY public.lendingbehavior."behaviorID";


--
-- Name: library; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.library (
    "resourceId" character varying NOT NULL,
    title character varying,
    author character varying,
    genre character varying,
    format character varying
);


ALTER TABLE public.library OWNER TO angledimensions;

--
-- Name: libraryresources; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.libraryresources (
    "resourceId" character varying NOT NULL,
    title character varying,
    author character varying,
    genre character varying,
    "publishedDate" character varying,
    "resourceType" character varying,
    "catelogedBy" character varying,
    format character varying
);


ALTER TABLE public.libraryresources OWNER TO angledimensions;

--
-- Name: members; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.members (
    "memberId" integer NOT NULL,
    fullname character varying NOT NULL,
    "membershipID" character varying NOT NULL,
    phone character varying NOT NULL,
    address character varying NOT NULL,
    "postCode" character varying NOT NULL,
    "dateEnrolled" timestamp without time zone,
    memberstatus character varying(50) DEFAULT 'Active'::character varying NOT NULL
);


ALTER TABLE public.members OWNER TO angledimensions;

--
-- Name: members_memberId_seq; Type: SEQUENCE; Schema: public; Owner: angledimensions
--

CREATE SEQUENCE public."members_memberId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."members_memberId_seq" OWNER TO angledimensions;

--
-- Name: members_memberId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: angledimensions
--

ALTER SEQUENCE public."members_memberId_seq" OWNED BY public.members."memberId";


--
-- Name: users; Type: TABLE; Schema: public; Owner: angledimensions
--

CREATE TABLE public.users (
    "userId" integer NOT NULL,
    username character varying NOT NULL,
    fullname character varying(225),
    password character varying,
    email character varying,
    role character varying,
    qualification character varying,
    experience character varying,
    "skillSet" character varying,
    grade character varying,
    contact character varying,
    responsibilities character varying
);


ALTER TABLE public.users OWNER TO angledimensions;

--
-- Name: users_userId_seq; Type: SEQUENCE; Schema: public; Owner: angledimensions
--

CREATE SEQUENCE public."users_userId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."users_userId_seq" OWNER TO angledimensions;

--
-- Name: users_userId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: angledimensions
--

ALTER SEQUENCE public."users_userId_seq" OWNED BY public.users."userId";


--
-- Name: lendingbehavior behaviorID; Type: DEFAULT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.lendingbehavior ALTER COLUMN "behaviorID" SET DEFAULT nextval('public."lendingbehavior_behaviorID_seq"'::regclass);


--
-- Name: members memberId; Type: DEFAULT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.members ALTER COLUMN "memberId" SET DEFAULT nextval('public."members_memberId_seq"'::regclass);


--
-- Name: users userId; Type: DEFAULT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.users ALTER COLUMN "userId" SET DEFAULT nextval('public."users_userId_seq"'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: borrowedbooks; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.borrowedbooks ("borrowId", "resourceId", "borrowedBy", "borrowedDate", "returnDate") FROM stdin;
\.


--
-- Data for Name: lendingbehavior; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.lendingbehavior ("behaviorID", "membershipID", "overdueCount", preference) FROM stdin;
4	6e9b3221-73e4-4a1a-8340-419cc0469aa6	0	\N
3	dede	0	Software Standards,Data Science
5	df3ae231-7559-48ee-b605-fc51bd0f2e74	0	Data Science,Non-Fiction,Software Standards,Python
2	64c4e21a-6678-4570-a364-c54cabbf31d3	0	Non-Fiction,Python,History,Data Science
8	8ccbd7b4-c3ae-4bb3-b4c7-fb049ebd025c	0	\N
9	Member50357D	0	Non-Fiction,Data Science
10	690cfc08-a60d-49e2-89d8-26df83243aed	0	Software Standards,Data Science
1	da1cec55-cc33-4aea-91b4-176faa2decef	0	Software Standards,Data Science
11	8d25ad65-9146-484d-9c81-56c2b6108216	0	Fiction,Non-Fiction,Software Standards,Python
7	weweww	0	Python,Fiction
6	b70c17ff-b05a-4cd0-8f96-d0394ffd359e	0	Python,Software Standards
\.


--
-- Data for Name: library; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.library ("resourceId", title, author, genre, format) FROM stdin;
a712a9a7-338c-4074-990e-0359df490dbe	Eustace	Eugo	fiction	hardcopy
547f9ed0-e607-42f6-a923-0dd8252c8571	Eustace	Eugo	fiction	hardcopy
\.


--
-- Data for Name: libraryresources; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.libraryresources ("resourceId", title, author, genre, "publishedDate", "resourceType", "catelogedBy", format) FROM stdin;
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.members ("memberId", fullname, "membershipID", phone, address, "postCode", "dateEnrolled", memberstatus) FROM stdin;
1	Trevion	8ccbd7b4-c3ae-4bb3-b4c7-fb049ebd025c	Eugo@1234	student	0000	2025-03-19 23:04:09.228122	Active
2	Trevionss	6e9b3221-73e4-4a1a-8340-419cc0469aa6	Eugo@1234	student	0000	2025-03-19 23:04:29.825865	Active
3	Eustace	b70c17ff-b05a-4cd0-8f96-d0394ffd359e	8798878	Lilongwe	000000	2025-03-19 23:10:46.366158	Active
4	Trevionss	e8dfcadf-c172-407b-a6d8-738f0a349c79	Eugo@1234	student	0000	2025-03-20 22:03:17.28994	Active
5	Iola Gill	da1cec55-cc33-4aea-91b4-176faa2decef	+1 (865) 518-9005	Veniam nulla sed do	At inventore invento	2025-03-21 00:56:13.00883	Active
7	Blair Day	dede	+1 (548) 859-6324	Dolorum id architect	Adipisci odio enim a	2025-03-21 21:05:10.669605	Active
10	Octavia Kennedy	64c4e21a-6678-4570-a364-c54cabbf31d3	+1 (224) 357-9683	Autem nemo soluta si	Mollitia minim perfe	2025-03-21 21:06:43.23046	Active
11	Echo Bauer	df3ae231-7559-48ee-b605-fc51bd0f2e74	+1 (167) 539-6508	Beatae et dolor et q	Commodo sit qui vol	2025-03-21 21:06:49.448337	Active
12	Tasha Whitney	8d25ad65-9146-484d-9c81-56c2b6108216	+1 (732) 962-4729	Molestiae obcaecati 	Optio odit quia atq	2025-03-21 21:07:13.427991	Active
13	Alea Glenn	690cfc08-a60d-49e2-89d8-26df83243aed	+1 (107) 633-7928	Doloribus porro cons	Ab assumenda aut per	2025-03-21 21:07:16.200106	Active
14	Linda	ww	Eugo@1234	student	0000	2025-03-23 12:11:22.127132	Active
15	Skyler Acosta	weweww	+1 (879) 916-3256	Enim ut quis volupta	Temporibus quo dolor	2025-03-23 12:17:44.126646	Active
18	Bethany Buckner	Member8378H4	+1 (727) 928-8741	Odit rerum quis et i	Tempor quo nobis fug	2025-03-23 12:20:44.546363	Active
19	Hedda Wilkins	Member50357D	+1 (751) 598-2773	In maiores ea conseq	Odit praesentium sun	2025-03-23 12:20:49.500732	Active
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: angledimensions
--

COPY public.users ("userId", username, fullname, password, email, role, qualification, experience, "skillSet", grade, contact, responsibilities) FROM stdin;
4	Linda	\N	$2b$12$KMIpe4uOElzcnsbAiowfwOzFoToDwQSWRIwUIixCm/TmmaNyoqprC	\N	student	\N	\N	\N	\N	\N	\N
5	Linda1	\N	$2b$12$JlBkzGNNGsCL/JWVcRWHeOPPqNJ6VEa5H1ZxAg4mCrXBi5nKSLhQi	\N	student	\N	\N	\N	\N	\N	\N
6	Linda2	\N	$2b$12$cWtSwZ2/Nt76hpo7fHRxzOQql0I3MU8E2R9aP4t2gPL3.LqY5hlMO	\N	student	\N	\N	\N	\N	\N	\N
7	Linda3	\N	$2b$12$xjKKU9RKkIegmJBfExlDa.qPcufYMNPyFr7HHLjfHyTtd3fcRwDtG	\N	student	\N	\N	\N	\N	\N	\N
2	Linda	Linda2s	$2b$12$Gmoj9uC365s6PXXCWWYIteUYRUB2bbB8sIaQrIzdQuw4fJ6noGtwW	\N	Lbrarian	Bachelor's Degree	5 years	Python, FastAPI, SQL	Senior	john.doe@example.com	{"adding books"}
3	Linda2	Linda2	$2b$12$QZ4s4yF/gbzTs/CqwS0igeYuR5IrqXzfyab61DOFHD0p.pGd0YkuK	\N	librarymanager	Bachelor's Degree	5 years	Python, FastAPI, SQL	Senior	john.doe@example.com	\N
1	eugo eustace		$2b$12$vWr7mnzS7d2MXAuFESsYu..pJkSKy6FgSgB9p4wgvDaEqS6n9h/MO	\N	cataloger				dweddw		\N
8	qolewe	\N	$2b$12$0kpywIqV3IlA2pxYPUyO..5.0cBD/w3Qet7oGgjK6xVtNBtBaBCtm	\N	User	\N	\N	\N	\N	\N	\N
9	desywawe	\N	$2b$12$26QIQBgJAnZkcKsw1nYBDOGEMQ/6J0iiRBlgu5rmMJSat7lQFrh3y	\N	User	\N	\N	\N	\N	\N	\N
10	geper	\N	$2b$12$.U0U.H13.UNRPXTYPeh8bOzWpwQOZYCu55gwT5UIPBPPzTK6H5vcG	\N	User	\N	\N	\N	\N	\N	\N
11	librarymanager	\N	$2b$12$l0ex1zf/M9jzJ56XaJm24.2b5KaKmIEBuRIjDt0OZOGYOI4XulRMS	\N	librarymanager	\N	\N	\N	\N	\N	\N
\.


--
-- Name: lendingbehavior_behaviorID_seq; Type: SEQUENCE SET; Schema: public; Owner: angledimensions
--

SELECT pg_catalog.setval('public."lendingbehavior_behaviorID_seq"', 11, true);


--
-- Name: members_memberId_seq; Type: SEQUENCE SET; Schema: public; Owner: angledimensions
--

SELECT pg_catalog.setval('public."members_memberId_seq"', 19, true);


--
-- Name: users_userId_seq; Type: SEQUENCE SET; Schema: public; Owner: angledimensions
--

SELECT pg_catalog.setval('public."users_userId_seq"', 11, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: borrowedbooks borrowedbooks_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.borrowedbooks
    ADD CONSTRAINT borrowedbooks_pkey PRIMARY KEY ("borrowId");


--
-- Name: lendingbehavior lendingbehavior_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.lendingbehavior
    ADD CONSTRAINT lendingbehavior_pkey PRIMARY KEY ("behaviorID");


--
-- Name: library library_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_pkey PRIMARY KEY ("resourceId");


--
-- Name: libraryresources libraryresources_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.libraryresources
    ADD CONSTRAINT libraryresources_pkey PRIMARY KEY ("resourceId");


--
-- Name: members members_membershipID_key; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT "members_membershipID_key" UNIQUE ("membershipID");


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY ("memberId");


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("userId", username);


--
-- Name: ix_borrowedbooks_borrowId; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_borrowedbooks_borrowId" ON public.borrowedbooks USING btree ("borrowId");


--
-- Name: ix_lendingbehavior_behaviorID; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_lendingbehavior_behaviorID" ON public.lendingbehavior USING btree ("behaviorID");


--
-- Name: ix_library_resourceId; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_library_resourceId" ON public.library USING btree ("resourceId");


--
-- Name: ix_libraryresources_resourceId; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_libraryresources_resourceId" ON public.libraryresources USING btree ("resourceId");


--
-- Name: ix_members_memberId; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_members_memberId" ON public.members USING btree ("memberId");


--
-- Name: ix_users_userId; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX "ix_users_userId" ON public.users USING btree ("userId");


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: angledimensions
--

CREATE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: borrowedbooks borrowedbooks_borrowedBy_fkey; Type: FK CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.borrowedbooks
    ADD CONSTRAINT "borrowedbooks_borrowedBy_fkey" FOREIGN KEY ("borrowedBy") REFERENCES public.members("membershipID");


--
-- Name: borrowedbooks borrowedbooks_resourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.borrowedbooks
    ADD CONSTRAINT "borrowedbooks_resourceId_fkey" FOREIGN KEY ("resourceId") REFERENCES public.libraryresources("resourceId");


--
-- Name: lendingbehavior lendingbehavior_membershipID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: angledimensions
--

ALTER TABLE ONLY public.lendingbehavior
    ADD CONSTRAINT "lendingbehavior_membershipID_fkey" FOREIGN KEY ("membershipID") REFERENCES public.members("membershipID");


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

