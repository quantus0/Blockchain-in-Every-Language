package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"
)


type Block struct {
	Index     int
	Timestamp string
	Data      string
	PrevHash  string
	Hash      string
}


func calculateHash(block Block) string {
	record := string(block.Index) + block.Timestamp + block.Data + block.PrevHash
	hash := sha256.New()
	hash.Write([]byte(record))
	return hex.EncodeToString(hash.Sum(nil))
}


func generateBlock(oldBlock Block, data string) Block {
	newBlock := Block{
		Index:     oldBlock.Index + 1,
		Timestamp: time.Now().String(),
		Data:      data,
		PrevHash:  oldBlock.Hash,
	}
	newBlock.Hash = calculateHash(newBlock)
	return newBlock
}


func isBlockValid(newBlock, oldBlock Block) bool {
	return oldBlock.Index+1 == newBlock.Index &&
		oldBlock.Hash == newBlock.PrevHash &&
		calculateHash(newBlock) == newBlock.Hash
}

func main() {
	genesisBlock := Block{
		Index:     0,
		Timestamp: time.Now().String(),
		Data:      "Genesis Block",
		PrevHash:  "",
	}
	genesisBlock.Hash = calculateHash(genesisBlock)

	blockchain := []Block{genesisBlock}

	


	newData := []string{"First block", "Second block", "Third block"}

	for _, data := range newData {
		newBlock := generateBlock(blockchain[len(blockchain)-1], data)
		if isBlockValid(newBlock, blockchain[len(blockchain)-1]) {
			blockchain = append(blockchain, newBlock)
		}
	}

	
	for _, block := range blockchain {
		fmt.Printf("Index: %d\nTimestamp: %s\nData: %s\nPrevHash: %s\nHash: %s\n\n",
			block.Index, block.Timestamp, block.Data, block.PrevHash, block.Hash)
	}
}
