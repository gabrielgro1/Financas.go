package service

import (
	"context"
	"errors"
	"financas/domain"
)

var ErrDescriptionRequired = errors.New("description is required")

type TransactionRepository interface {
	Create(ctx context.Context, transaction domain.Transaction) error
}

type TransactionService struct {
	repository TransactionRepository
}

func NewTransactionService(repository TransactionRepository) *TransactionService {
	return &TransactionService{repository: repository}
}

type CreateTransactionInput struct {
	Description string  `json:"description"`
	Amount      float64 `json:"amount"`
	Type        string  `json:"type"`
	Date        string  `json:"date"`
}

func (s* TransactionService) ValidadeCreate(input CreateTransactionInput) error {
	return nil
}