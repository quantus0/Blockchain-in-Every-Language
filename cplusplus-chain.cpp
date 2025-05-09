#include <iostream>
#include <sstream>
#include <vector>
#include <ctime>
#include <openssl/sha.h>

using namespace std;

string sha256(const string str) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)str.c_str(), str.size(), hash);
    stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i)
        ss << hex << (int)hash[i];
    return ss.str();
}

class Block {
public:
    int index;
    string data;
    string previousHash;
    string hash;
    time_t timestamp;

    Block(int idx, const string& d, const string& prevHash)
        : index(idx), data(d), previousHash(prevHash), timestamp(time(nullptr)) {
        hash = calculateHash();
    }

    string calculateHash() const {
        stringstream ss;
        ss << index << timestamp << data << previousHash;
        return sha256(ss.str());
    }
};

class Blockchain {
private:
    vector<Block> chain;

    Block createGenesisBlock() {
        return Block(0, "Genesis Block", "0");
    }

public:
    Blockchain() {
        chain.push_back(createGenesisBlock());
    }

    void addBlock(const string& data) {
        Block newBlock(chain.size(), data, chain.back().hash);
        chain.push_back(newBlock);
    }

    void printChain() const {
        for (const Block& block : chain) {
            cout << "Block " << block.index << " [" << block.hash << "]\n";
            cout << "  Previous: " << block.previousHash << "\n";
            cout << "  Data: " << block.data << "\n";
            cout << "  Time: " << ctime(&block.timestamp) << "\n";
        }
    }
};

int main() {
    Blockchain myBlockchain;
    myBlockchain.addBlock("First transaction");
    myBlockchain.addBlock("Second transaction");
    myBlockchain.printChain();
    return 0;
}
