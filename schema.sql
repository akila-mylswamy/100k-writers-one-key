--
-- PostgreSQL database dump
--

\restrict r7mTMAMMgHj9v1ojTD4vr0UvXZtwoH1t9ZzUREGwrSDPgX0OZ0vi6zU49wdDpgd

-- Dumped from database version 18.7 (Homebrew)
-- Dumped by pg_dump version 18.7 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: counters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.counters (
    id integer NOT NULL,
    value bigint DEFAULT 0 NOT NULL
);


--
-- Name: counters counters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.counters
    ADD CONSTRAINT counters_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict r7mTMAMMgHj9v1ojTD4vr0UvXZtwoH1t9ZzUREGwrSDPgX0OZ0vi6zU49wdDpgd

