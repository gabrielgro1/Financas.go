package service

import (

)

type TransactionService struct {}

func NewTransactionService () *TransactionService {
	return &TransactionService{}
}

type CreateTransactionService struct {

	Description string `json:"description"`
	Amount float64 `json:"Amount"`
	Type string `json:"type"`
	Date string `json:"date"`

}