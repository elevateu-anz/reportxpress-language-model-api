CREATE TABLE [dbo].[branch] (
    [branch_id]      INT           IDENTITY (101, 1) NOT NULL,
    [branch_name]    VARCHAR (50)  NOT NULL,
    [branch_address] VARCHAR (250) NOT NULL,
    [assets]         INT           NULL,
    CONSTRAINT [PK_branch] PRIMARY KEY CLUSTERED ([branch_id] ASC)
); 

CREATE TABLE [dbo].[banker] (
    [banker_id]      INT           IDENTITY (1001, 1) NOT NULL,
    [banker_name]    VARCHAR (50)  NOT NULL,
    [branch_id]      INT           NOT NULL,
    CONSTRAINT [PK_banker] PRIMARY KEY CLUSTERED ([banker_id] ASC),
    CONSTRAINT FK_banker_branch FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

CREATE TABLE [dbo].[account] (
    [account_id]         BIGINT        IDENTITY (20240000101, 1) NOT NULL,
    [account_balance]    INT           NOT NULL,
    [account_type]       VARCHAR (50)  NOT NULL,
    [branch_id]          INT           NOT NULL,
    CONSTRAINT [PK_account] PRIMARY KEY CLUSTERED ([account_id] ASC),
    CONSTRAINT FK_account_branch FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

CREATE TABLE [dbo].[customer] (
    [customer_id]        BIGINT         IDENTITY (202400001, 1) NOT NULL,
    [customer_name]      VARCHAR(50)    NOT NULL,
    [dob]                DATE           NOT NULL,
    [mobile_no]          VARCHAR(20)    NOT NULL,
    [account_id]         BIGINT         NOT NULL,
    CONSTRAINT [PK_customer] PRIMARY KEY CLUSTERED ([customer_id] ASC),
    CONSTRAINT [UQ_customer] UNIQUE ([mobile_no]),
    CONSTRAINT FK_customer_account FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE [dbo].[credit_card] (
    [credit_card_id]         INT           IDENTITY (1, 1) NOT NULL,
    [expiry_date]            DATE          NOT NULL,
    [card_limit]             INT           NOT NULL,
    [credit_card_num]        VARCHAR (19)  NOT NULL,
    [account_id]             BIGINT        NOT NULL,
    [customer_id]            BIGINT        NOT NULL,
    CONSTRAINT [PK_credit_card] PRIMARY KEY CLUSTERED ([credit_card_id] ASC),
    CONSTRAINT FK_credit_card_account FOREIGN KEY (account_id) REFERENCES account(account_id),
    CONSTRAINT FK_credit_card_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE [dbo].[transaction] (
    [transaction_id]     BIGINT        IDENTITY (2024000001, 1) NOT NULL,         
    [account_id]         BIGINT        NOT NULL,
    [customer_id]        BIGINT        NOT NULL,
    [amount]             INT           NOT NULL,
    CONSTRAINT [PK_transaction] PRIMARY KEY CLUSTERED ([transaction_id] ASC),
    CONSTRAINT FK_transaction_account FOREIGN KEY (account_id) REFERENCES account(account_id),
    CONSTRAINT FK_transaction_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE [dbo].[loan] (
    [loan_id]            BIGINT        IDENTITY (20240001, 1) NOT NULL,
    [issued_amount]      INT           NOT NULL,
    [remaining_amount]   INT           NOT NULL,
    [branch_id]          INT           NOT NULL,
    [account_id]         BIGINT        NOT NULL,
    CONSTRAINT [PK_loan] PRIMARY KEY CLUSTERED ([loan_id] ASC),
    CONSTRAINT FK_loan_branch FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
    CONSTRAINT FK_loan_account FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE [dbo].[borrower] (
    [borrower_id]     BIGINT        IDENTITY (2024001, 1) NOT NULL,
    [loan_id]         BIGINT        NOT NULL,
    [customer_id]     BIGINT        NOT NULL,
    CONSTRAINT [PK_borrower] PRIMARY KEY CLUSTERED ([borrower_id] ASC),
    CONSTRAINT FK_borrower_loan FOREIGN KEY (loan_id) REFERENCES loan(loan_id),
    CONSTRAINT FK_borrower_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE [dbo].[loan_payment] (
    [loan_payment_id]      INT           IDENTITY (1, 1) NOT NULL,
    [loan_id]              BIGINT        NOT NULL,
    [amount]               INT           NOT NULL,
    CONSTRAINT [PK_loan_payment] PRIMARY KEY CLUSTERED ([loan_payment_id] ASC),
    CONSTRAINT FK_loan_payment_loan FOREIGN KEY (loan_id) REFERENCES loan(loan_id)
);

