CREATE TABLE "User"
(   
	 "idUser" SERIAL PRIMARY KEY,
	 "name" varchar(50) NOT NULL,
	 "password" varchar(50) NOT NULL,
	 "email" varchar(50) NOT NULL,
	 "status" boolean NOT NULL DEFAULT TRUE
);
CREATE TABLE "Student"
(   
	"idStudent" SERIAL PRIMARY KEY,
	"name" varchar(50) NOT NULL,
	"lastName" varchar(50) NOT NULL,
	"mothersthestName" varchar(50) NOT NULL,
	"enrollment" varchar(50) NOT NULL,
	"birthdate" date NOT NULL,
	"curp" char (18) NOT NULL,
	"phone" char (10) NOT NULL,
	"rfc" char (13) NOT NULL,
	"socialSegurity" char (11) NOT NULL,
	"idEmployee" INT NOT NULL,
	"status" boolean NOT NULL DEFAULT TRUE,
	"idUserCreate" INT NOT NULL,
	"dateCreate" DATE NOT NULL,
	"idUserModified" INT NOT NULL,
	"dateModified" DATE NOT NULL
);
CREATE TABLE "CompanyStudent" (
	"IdCompanyStudent" SERIAL PRIMARY KEY,
	"date" Date NULL,
	"workplace" varchar(50) NOT NULL,
	"idStudent" INT NOT NULL,
	"status" boolean NOT NULL DEFAULT TRUE,
	"idUserCreate" INT NOT NULL,
	"dateCreate" DATE NOT NULL,
	"idUserModified" INT NOT NULL,
	"dateModified" DATE NOT NULL
);
INSERT INTO "User" ("name","password", "email")
VALUES ('Nallely', '123','toledo@');

INSERT INTO "Student" ("name","lastName","mothersthestName","enrollment","birthdate","curp","phone","rfc","socialSegurity","idEmployee","idUserCreate","dateCreate","idUserModified","dateModified")
VALUES ('Nallely','Toledo','Alonso','I15171917','1996-06-09','TOASMNL000NLLN9654','8667882323','TOASMNL000NLL','44180032043',1,1,NOW(),1,NOW()),
       ('Alberto','Salazar','Zuñiga','I18050517','2000-04-08','SAZA000408HCLLXLA6','8661222321','SAZA000408K61','44180032089',2,1,NOW(),1,NOW()),
	   ('Antonio','Perez','Gaitan','I23050517','2003-08-20','PEGA030820HCLLXKLR','8664322321','PEGA030820HCL','44180032090',3,1,NOW(),1,NOW()),
	   ('Maria','Rivera','Soledad','I20050517','2005-01-25','RISM000408HCLLXLA6','8662332321','RISM000408HCL','44180032011',4,1,NOW(),1,NOW()),
	   ('Bertha','Ibarra','Vazquez','I17050517','2007-09-17','VAVB000408HCLLXLO6','8666542321','VAVB000408HCL','44180032055',5,1,NOW(),1,NOW());
	   
select * from  "User";

