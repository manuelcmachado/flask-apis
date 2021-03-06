USE [MMachadoDB]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- =======================================================================================================
-- Author:	Manuel Machado
-- Create date: 2022-06-23
-- Description:	The procedure extracts current sales data from AdventureWorksDW2019 Ordered on 2014-01-28 
--				Or after
--
-- Parameters: None
--
-- =======================================================================================================

ALTER PROCEDURE [AdventureWorks].[CurrentInternetSales]  
	
AS
BEGIN
	
	SET NOCOUNT ON;
	SET XACT_ABORT ON;

	WITH ProductSales AS(
		SELECT	B.ProductLine, B.ModelName, B.EnglishProductName, B.Color, A.OrderQuantity,
                CAST(A.OrderDate AS DATE) AS OrderDate, CAST(A.ShipDate AS DATE) AS ShipDate,  
				A.TotalProductCost, B.ListPrice,  A.UnitPrice, A.SalesAmount, A.TaxAmt AS TaxAmount, 
				A.SalesOrderNumber, C.CurrencyName, A.SalesTerritoryKey
		FROM AdventureWorksDW2019.dbo.FactInternetSales A
			INNER JOIN AdventureWorksDW2019.dbo.DimProduct B ON B.ProductKey = A.ProductKey
			INNER JOIN AdventureWorksDW2019.dbo.DimCurrency C ON C.CurrencyKey = A.CurrencyKey
		WHERE B.Status = 'Current'
	)
	SELECT	RunDate = GETDATE(),
			B.EnglishProductName, B.ModelName, B.Color, B.OrderQuantity, B.OrderDate, B.ShipDate,
            B.TotalProductCost, B.ListPrice, B.UnitPrice, B.SalesAmount, B.TaxAmount, B.SalesOrderNumber, B.CurrencyName, 
            A.SalesTerritoryCountry, A.SalesTerritoryGroup
	FROM AdventureWorksDW2019.dbo.DimSalesTerritory A 
	INNER JOIN ProductSales B ON B.SalesTerritoryKey = A.SalesTerritoryKey
	WHERE OrderDate >= '2014-01-28';
END


