# EC530-Smart-Document-Analyzer
Smart Document Analyzer

# Database Schema Plan
User Table:
-UserID (Primary Key)
-Username
-Password (Hashed and salted)

Document Table:
-DocumentID (Primary Key)
-UserID (Foreign Key)
-Title
-Content (Text/BLOB)
-FileType
-UploadDate

Keyword Table:
-KeywordID (Primary Key)
-KeywordText

DocumentKeyword Table (Many-to-Many):
-DocumentID (Foreign Key)
-KeywordID (Foreign Key)

Paragraph Table:
-ParagraphID (Primary Key)
-DocumentID (Foreign Key)
-Content (Text/BLOB)
-Positive/Negative/Neutral (Boolean)
-PublishDate

KeywordSearch Table (Many-to-Many):
-KeywordID (Foreign Key)
-Source
-SearchResult (Text/BLOB)

Definition Table:
-KeywordID (Foreign Key)
-Source
-Definition (Text/BLOB)

Summary Table:
-DocumentID (Foreign Key)
-SummaryText (Text/BLOB)

WebContent Table:
-ContentID (Primary Key)
-UserID (Foreign Key)
-Content (Text/BLOB)

EntityRecognition Table:
-EntityID (Primary Key)
-DocumentID (Foreign Key)
-EntityType
-EntityText