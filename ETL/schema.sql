DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS game1;
DROP TABLE IF EXISTS athlete;
DROP TABLE IF EXISTS medal;
DROP TABLE IF EXISTS master;

CREATE TABLE "country" (
    "country_id" VARCHAR NOT NULL,
    "Country" VARCHAR NOT NULL,
    "Code" VARCHAR   NOT NULL,
    "Population" FLOAT,
    "GDP" FLOAT,
    CONSTRAINT "pk_country" PRIMARY KEY (
        "country_id"
     )
);

SELECT * FROM "country"

CREATE TABLE "game1" (
    "event_id" VARCHAR not null,
    "Year" INT   NOT NULL,
    "City" varchar not null,
    "Sport" varchar not null,
    "Discipline" varchar not null,
    "Event" varchar not null,
    "Season" varchar not null,
    CONSTRAINT "pk_game1" PRIMARY KEY (
        "event_id"
     )
);

SELECT * FROM "game1"

CREATE TABLE "athlete" (
    "country_id" VARCHAR,
    "Athlete" varchar,
    "Athlete_id" VARCHAR not null,
    "Gender" varchar,
    CONSTRAINT "pk_athlete" PRIMARY KEY (
        "Athlete_id"
     )
);

SELECT * FROM "athlete"

CREATE TABLE "medal" (
    "medal_id" VARCHAR NOT NULL,
    "Medal" VARCHAR not null,
     CONSTRAINT "pk_Medal" PRIMARY KEY(
	"medal_id"
)
);

SELECT * FROM "medal"

CREATE TABLE "master" (
    "event_id" VARCHAR not null,
    "Athlete_id" VARCHAR NOT NULL,
    "medal_id" VARCHAR
);

SELECT * FROM "master"