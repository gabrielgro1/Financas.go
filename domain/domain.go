package domain

import "time"

type TransactionType string

const (
	TransactionTypeIncome  TransactionType = "income"
	TransactionTypeExpense TransactionType = "expense"
)

type Transaction struct {
	ID          int
	Description string
	AmountCents int
	Type        TransactionType
	Date        time.Time
}
