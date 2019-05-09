DROP DATABASE IF EXISTS CFEA;
CREATE DATABASE CFEA;
DROP TABLE IF EXISTS meta;

CREATE TABLE meta(
  sample char(20),
  GSM char(20),
  diseases char(20),
  PMID char(20),
  technical char(20),
  source char(20),
  stage char(20),
  adapter_content char(5),
  duplication_level char(5),
  base_quality char(20),
  basic_statistics char(20),
  overrepresented_sequences char(20),
  overall_alignment_rate char(20)
)ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

