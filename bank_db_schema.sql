CREATE TABLE [dbo].[branch] (
    [branch_id]      INT           IDENTITY (101, 1) NOT NULL,
    [branch_name]    VARCHAR (50)  NOT NULL,
    [branch_address] VARCHAR (250) NOT NULL,
    [assets]         INT           NULL,
    CONSTRAINT [PK_branch] PRIMARY KEY CLUSTERED ([branch_id] ASC)
);
