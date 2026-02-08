import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Pumpnotdump } from "../target/types/pumpnotdump";
import { 
  PublicKey, 
  Keypair, 
  SystemProgram, 
  SYSVAR_RENT_PUBKEY 
} from "@solana/web3.js";
import {
  TOKEN_PROGRAM_ID,
  createMint,
  getOrCreateAssociatedTokenAccount,
  mintTo,
} from "@solana/spl-token";
import { assert } from "chai";

describe("pumpnotdump", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.Pumpnotdump as Program<Pumpnotdump>;
  
  const platformAuthority = provider.wallet as anchor.Wallet;
  const agentWallet = Keypair.generate();
  const agentWallet2 = Keypair.generate();
  
  let platformStatePDA: PublicKey;
  let agentRegistryPDA: PublicKey;
  let agentRegistry2PDA: PublicKey;
  let tokenMint: PublicKey;
  let launchPadPDA: PublicKey;
  let treasuryVaultPDA: PublicKey;
  let rugScorePDA: PublicKey;

  // Helper to find PDAs
  const findPlatformStatePDA = () => {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("platform")],
      program.programId
    );
  };

  const findAgentRegistryPDA = (agentWallet: PublicKey) => {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("agent"), agentWallet.toBuffer()],
      program.programId
    );
  };

  const findLaunchPadPDA = (agentRegistry: PublicKey, tokenMint: PublicKey) => {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("launch"), agentRegistry.toBuffer(), tokenMint.toBuffer()],
      program.programId
    );
  };

  const findTreasuryVaultPDA = (agentRegistry: PublicKey, tokenMint: PublicKey) => {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("treasury"), agentRegistry.toBuffer(), tokenMint.toBuffer()],
      program.programId
    );
  };

  const findRugScorePDA = (tokenMint: PublicKey) => {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("rug_score"), tokenMint.toBuffer()],
      program.programId
    );
  };

  before(async () => {
    // Airdrop SOL to test wallets
    const airdropSignature = await provider.connection.requestAirdrop(
      agentWallet.publicKey,
      2 * anchor.web3.LAMPORTS_PER_SOL
    );
    await provider.connection.confirmTransaction(airdropSignature);

    const airdropSignature2 = await provider.connection.requestAirdrop(
      agentWallet2.publicKey,
      2 * anchor.web3.LAMPORTS_PER_SOL
    );
    await provider.connection.confirmTransaction(airdropSignature2);

    [platformStatePDA] = findPlatformStatePDA();
    [agentRegistryPDA] = findAgentRegistryPDA(agentWallet.publicKey);
    [agentRegistry2PDA] = findAgentRegistryPDA(agentWallet2.publicKey);
  });

  describe("Platform Initialization", () => {
    it("Initializes platform state", async () => {
      const tx = await program.methods
        .initializePlatform(100, 30) // 1% fee, 30 day min lock
        .accounts({
          platformState: platformStatePDA,
          authority: platformAuthority.publicKey,
          systemProgram: SystemProgram.programId,
        })
        .rpc();

      console.log("Initialize platform tx:", tx);

      const platformState = await program.account.platformState.fetch(platformStatePDA);
      
      assert.equal(platformState.platformFeeBps, 100);
      assert.equal(platformState.minLiquidityLockDays, 30);
      assert.equal(platformState.isPaused, false);
      assert.equal(platformState.totalAgentsRegistered.toNumber(), 0);
      assert.equal(platformState.totalTokensLaunched.toNumber(), 0);
    });
  });

  describe("Agent Registration", () => {
    it("Registers an AI agent with metadata", async () => {
      const tx = await program.methods
        .registerAgent(
          "Skipper AI",
          "AI agent building on Solana",
          "@skipperai",
          "https://skipper.ai",
          "https://github.com/skipperai"
        )
        .accounts({
          agentRegistry: agentRegistryPDA,
          agentWallet: agentWallet.publicKey,
          platformState: platformStatePDA,
          systemProgram: SystemProgram.programId,
        })
        .signers([agentWallet])
        .rpc();

      console.log("Register agent tx:", tx);

      const agentRegistry = await program.account.agentRegistry.fetch(agentRegistryPDA);
      
      assert.equal(agentRegistry.name, "Skipper AI");
      assert.equal(agentRegistry.description, "AI agent building on Solana");
      assert.equal(agentRegistry.twitterHandle, "@skipperai");
      assert.equal(agentRegistry.isVerified, false);
      assert.equal(agentRegistry.tokensLaunched, 0);

      const platformState = await program.account.platformState.fetch(platformStatePDA);
      assert.equal(platformState.totalAgentsRegistered.toNumber(), 1);
    });

    it("Fails to register agent without social links", async () => {
      try {
        await program.methods
          .registerAgent(
            "No Social Agent",
            "Agent with no social links",
            "",
            "",
            ""
          )
          .accounts({
            agentRegistry: agentRegistry2PDA,
            agentWallet: agentWallet2.publicKey,
            platformState: platformStatePDA,
            systemProgram: SystemProgram.programId,
          })
          .signers([agentWallet2])
          .rpc();
        
        assert.fail("Should have failed without social links");
      } catch (err) {
        assert.include(err.toString(), "NoSocialLinks");
      }
    });

    it("Registers second agent with only website", async () => {
      await program.methods
        .registerAgent(
          "Second Agent",
          "Another AI agent",
          "",
          "https://agent2.ai",
          ""
        )
        .accounts({
          agentRegistry: agentRegistry2PDA,
          agentWallet: agentWallet2.publicKey,
          platformState: platformStatePDA,
          systemProgram: SystemProgram.programId,
        })
        .signers([agentWallet2])
        .rpc();

      const platformState = await program.account.platformState.fetch(platformStatePDA);
      assert.equal(platformState.totalAgentsRegistered.toNumber(), 2);
    });
  });

  describe("Platform Admin Actions", () => {
    it("Platform admin can verify an agent", async () => {
      const tx = await program.methods
        .verifyAgent()
        .accounts({
          agentRegistry: agentRegistryPDA,
          platformAuthority: platformAuthority.publicKey,
          platformState: platformStatePDA,
          authority: platformAuthority.publicKey,
        })
        .rpc();

      console.log("Verify agent tx:", tx);

      const agentRegistry = await program.account.agentRegistry.fetch(agentRegistryPDA);
      assert.equal(agentRegistry.isVerified, true);
    });

    it("Non-admin cannot verify agent", async () => {
      try {
        await program.methods
          .verifyAgent()
          .accounts({
            agentRegistry: agentRegistry2PDA,
            platformAuthority: agentWallet.publicKey,
            platformState: platformStatePDA,
            authority: platformAuthority.publicKey,
          })
          .signers([agentWallet])
          .rpc();
        
        assert.fail("Non-admin should not be able to verify");
      } catch (err) {
        assert.include(err.toString(), "UnauthorizedPlatformAction");
      }
    });
  });

  describe("Token Launch", () => {
    it("Launches a token with rug protection", async () => {
      tokenMint = Keypair.generate();
      
      [launchPadPDA] = findLaunchPadPDA(agentRegistryPDA, tokenMint.publicKey);
      [treasuryVaultPDA] = findTreasuryVaultPDA(agentRegistryPDA, tokenMint.publicKey);
      [rugScorePDA] = findRugScorePDA(tokenMint.publicKey);

      const teamTokenAccount = await getOrCreateAssociatedTokenAccount(
        provider.connection,
        agentWallet,
        tokenMint.publicKey,
        agentWallet.publicKey
      );

      const totalSupply = new anchor.BN(1_000_000_000_000); // 1M tokens with 9 decimals
      const liquidityPercent = 60; // 60%
      const teamPercent = 15; // 15%
      const liquidityLockDays = 90; // 90 days
      const treasuryLockDays = 30; // 30 days
      const maxWithdrawalPerWeek = new anchor.BN(10_000_000_000); // 10K tokens per week

      const tx = await program.methods
        .launchToken(
          totalSupply,
          liquidityPercent,
          teamPercent,
          liquidityLockDays,
          treasuryLockDays,
          maxWithdrawalPerWeek
        )
        .accounts({
          launchPad: launchPadPDA,
          agentRegistry: agentRegistryPDA,
          tokenMint: tokenMint.publicKey,
          treasuryVault: treasuryVaultPDA,
          rugScore: rugScorePDA,
          teamTokenAccount: teamTokenAccount.address,
          agentWallet: agentWallet.publicKey,
          platformState: platformStatePDA,
          tokenProgram: TOKEN_PROGRAM_ID,
          systemProgram: SystemProgram.programId,
          rent: SYSVAR_RENT_PUBKEY,
        })
        .signers([agentWallet, tokenMint])
        .rpc();

      console.log("Launch token tx:", tx);

      // Verify LaunchPad
      const launchPad = await program.account.launchPad.fetch(launchPadPDA);
      assert.equal(launchPad.totalSupply.toString(), totalSupply.toString());
      assert.equal(launchPad.isActive, true);

      // Verify RugScore
      const rugScore = await program.account.rugScore.fetch(rugScorePDA);
      assert.equal(rugScore.liquidityLockPercent, liquidityPercent);
      assert.equal(rugScore.teamWalletConcentration, teamPercent);
      assert.equal(rugScore.isSocialVerified, true);
      assert.isAbove(rugScore.score, 0);
      console.log("Initial rug score:", rugScore.score);

      // Verify TreasuryVault
      const treasuryVault = await program.account.treasuryVault.fetch(treasuryVaultPDA);
      assert.equal(treasuryVault.authority.toString(), agentWallet.publicKey.toString());
      assert.equal(treasuryVault.requiresMultisig, false);

      // Verify platform state updated
      const platformState = await program.account.platformState.fetch(platformStatePDA);
      assert.equal(platformState.totalTokensLaunched.toNumber(), 1);

      // Verify agent registry updated
      const agentRegistry = await program.account.agentRegistry.fetch(agentRegistryPDA);
      assert.equal(agentRegistry.tokensLaunched, 1);
    });

    it("Fails to launch token with insufficient liquidity", async () => {
      const badTokenMint = Keypair.generate();
      const [badLaunchPad] = findLaunchPadPDA(agentRegistryPDA, badTokenMint.publicKey);
      const [badTreasury] = findTreasuryVaultPDA(agentRegistryPDA, badTokenMint.publicKey);
      const [badRugScore] = findRugScorePDA(badTokenMint.publicKey);

      const teamTokenAccount = await getOrCreateAssociatedTokenAccount(
        provider.connection,
        agentWallet,
        badTokenMint.publicKey,
        agentWallet.publicKey
      );

      try {
        await program.methods
          .launchToken(
            new anchor.BN(1_000_000_000_000),
            30, // Only 30% liquidity - should fail (min 50%)
            15,
            90,
            30,
            new anchor.BN(10_000_000_000)
          )
          .accounts({
            launchPad: badLaunchPad,
            agentRegistry: agentRegistryPDA,
            tokenMint: badTokenMint.publicKey,
            treasuryVault: badTreasury,
            rugScore: badRugScore,
            teamTokenAccount: teamTokenAccount.address,
            agentWallet: agentWallet.publicKey,
            platformState: platformStatePDA,
            tokenProgram: TOKEN_PROGRAM_ID,
            systemProgram: SystemProgram.programId,
            rent: SYSVAR_RENT_PUBKEY,
          })
          .signers([agentWallet, badTokenMint])
          .rpc();

        assert.fail("Should have failed with insufficient liquidity");
      } catch (err) {
        assert.include(err.toString(), "InsufficientLiquidityLock");
      }
    });

    it("Fails to launch token with excessive team allocation", async () => {
      const badTokenMint = Keypair.generate();
      const [badLaunchPad] = findLaunchPadPDA(agentRegistryPDA, badTokenMint.publicKey);
      const [badTreasury] = findTreasuryVaultPDA(agentRegistryPDA, badTokenMint.publicKey);
      const [badRugScore] = findRugScorePDA(badTokenMint.publicKey);

      const teamTokenAccount = await getOrCreateAssociatedTokenAccount(
        provider.connection,
        agentWallet,
        badTokenMint.publicKey,
        agentWallet.publicKey
      );

      try {
        await program.methods
          .launchToken(
            new anchor.BN(1_000_000_000_000),
            60,
            25, // 25% team allocation - should fail (max 20%)
            90,
            30,
            new anchor.BN(10_000_000_000)
          )
          .accounts({
            launchPad: badLaunchPad,
            agentRegistry: agentRegistryPDA,
            tokenMint: badTokenMint.publicKey,
            treasuryVault: badTreasury,
            rugScore: badRugScore,
            teamTokenAccount: teamTokenAccount.address,
            agentWallet: agentWallet.publicKey,
            platformState: platformStatePDA,
            tokenProgram: TOKEN_PROGRAM_ID,
            systemProgram: SystemProgram.programId,
            rent: SYSVAR_RENT_PUBKEY,
          })
          .signers([agentWallet, badTokenMint])
          .rpc();

        assert.fail("Should have failed with excessive team allocation");
      } catch (err) {
        assert.include(err.toString(), "ExcessiveTeamAllocation");
      }
    });
  });

  describe("Rug Score Updates", () => {
    it("Agent can update their own rug score", async () => {
      const oldScore = (await program.account.rugScore.fetch(rugScorePDA)).score;

      const tx = await program.methods
        .updateRugScore(
          70, // Increase liquidity lock to 70%
          10, // Decrease team concentration to 10%
          true, // Contract verified
          null
        )
        .accounts({
          rugScore: rugScorePDA,
          tokenMint: tokenMint.publicKey,
          launchPad: launchPadPDA,
          agentRegistry: agentRegistryPDA,
          agentWallet: agentWallet.publicKey,
          platformState: platformStatePDA,
        })
        .signers([agentWallet])
        .rpc();

      console.log("Update rug score tx:", tx);

      const rugScore = await program.account.rugScore.fetch(rugScorePDA);
      assert.equal(rugScore.liquidityLockPercent, 70);
      assert.equal(rugScore.teamWalletConcentration, 10);
      assert.equal(rugScore.isContractVerified, true);
      assert.isAbove(rugScore.score, oldScore);
      console.log("Updated rug score:", rugScore.score, "(was:", oldScore + ")");
    });

    it("Platform admin can update rug score", async () => {
      await program.methods
        .updateRugScore(
          null,
          null,
          null,
          true // Verify social
        )
        .accounts({
          rugScore: rugScorePDA,
          tokenMint: tokenMint.publicKey,
          launchPad: launchPadPDA,
          agentRegistry: agentRegistryPDA,
          agentWallet: platformAuthority.publicKey,
          platformState: platformStatePDA,
        })
        .rpc();

      const rugScore = await program.account.rugScore.fetch(rugScorePDA);
      assert.equal(rugScore.isSocialVerified, true);
    });

    it("Non-authorized user cannot update rug score", async () => {
      try {
        await program.methods
          .updateRugScore(80, null, null, null)
          .accounts({
            rugScore: rugScorePDA,
            tokenMint: tokenMint.publicKey,
            launchPad: launchPadPDA,
            agentRegistry: agentRegistryPDA,
            agentWallet: agentWallet2.publicKey,
            platformState: platformStatePDA,
          })
          .signers([agentWallet2])
          .rpc();

        assert.fail("Non-authorized user should not be able to update");
      } catch (err) {
        assert.include(err.toString(), "UnauthorizedPlatformAction");
      }
    });
  });

  describe("Treasury Management", () => {
    let standaloneTreasuryPDA: PublicKey;
    let treasuryTokenMint: Keypair;
    let treasuryTokenAccount: any;

    it("Creates a standalone treasury vault", async () => {
      treasuryTokenMint = Keypair.generate();
      [standaloneTreasuryPDA] = findTreasuryVaultPDA(
        agentRegistryPDA,
        treasuryTokenMint.publicKey
      );

      const tx = await program.methods
        .createTreasury(
          7, // 7 day time lock
          new anchor.BN(100_000_000_000), // 100K tokens per period
          604800, // 7 days in seconds
          [], // No multisig
          0
        )
        .accounts({
          treasuryVault: standaloneTreasuryPDA,
          agentRegistry: agentRegistryPDA,
          tokenMint: treasuryTokenMint.publicKey,
          agentWallet: agentWallet.publicKey,
          systemProgram: SystemProgram.programId,
        })
        .signers([agentWallet])
        .rpc();

      console.log("Create treasury tx:", tx);

      const treasuryVault = await program.account.treasuryVault.fetch(standaloneTreasuryPDA);
      assert.equal(treasuryVault.authority.toString(), agentWallet.publicKey.toString());
      assert.equal(treasuryVault.requiresMultisig, false);
      assert.equal(treasuryVault.maxWithdrawalPerPeriod.toString(), "100000000000");
    });

    it("Fails to create treasury with too short time lock", async () => {
      const badMint = Keypair.generate();
      const [badTreasury] = findTreasuryVaultPDA(agentRegistryPDA, badMint.publicKey);

      try {
        await program.methods
          .createTreasury(
            5, // Only 5 days - should fail (min 7)
            new anchor.BN(100_000_000_000),
            604800,
            [],
            0
          )
          .accounts({
            treasuryVault: badTreasury,
            agentRegistry: agentRegistryPDA,
            tokenMint: badMint.publicKey,
            agentWallet: agentWallet.publicKey,
            systemProgram: SystemProgram.programId,
          })
          .signers([agentWallet])
          .rpc();

        assert.fail("Should have failed with short time lock");
      } catch (err) {
        assert.include(err.toString(), "TreasuryLockTooShort");
      }
    });
  });

  describe("Score Calculation", () => {
    it("Calculates perfect score correctly", async () => {
      const perfectTokenMint = Keypair.generate();
      const [perfectLaunchPad] = findLaunchPadPDA(agentRegistryPDA, perfectTokenMint.publicKey);
      const [perfectTreasury] = findTreasuryVaultPDA(agentRegistryPDA, perfectTokenMint.publicKey);
      const [perfectRugScore] = findRugScorePDA(perfectTokenMint.publicKey);

      const teamTokenAccount = await getOrCreateAssociatedTokenAccount(
        provider.connection,
        agentWallet,
        perfectTokenMint.publicKey,
        agentWallet.publicKey
      );

      await program.methods
        .launchToken(
          new anchor.BN(1_000_000_000_000),
          100, // 100% liquidity locked
          0,   // 0% team allocation
          365, // 1 year lock
          30,
          new anchor.BN(10_000_000_000)
        )
        .accounts({
          launchPad: perfectLaunchPad,
          agentRegistry: agentRegistryPDA,
          tokenMint: perfectTokenMint.publicKey,
          treasuryVault: perfectTreasury,
          rugScore: perfectRugScore,
          teamTokenAccount: teamTokenAccount.address,
          agentWallet: agentWallet.publicKey,
          platformState: platformStatePDA,
          tokenProgram: TOKEN_PROGRAM_ID,
          systemProgram: SystemProgram.programId,
          rent: SYSVAR_RENT_PUBKEY,
        })
        .signers([agentWallet, perfectTokenMint])
        .rpc();

      // Update to perfect score
      await program.methods
        .updateRugScore(
          100, // 100% liquidity
          0,   // 0% team
          true, // Verified contract
          true  // Verified social
        )
        .accounts({
          rugScore: perfectRugScore,
          tokenMint: perfectTokenMint.publicKey,
          launchPad: perfectLaunchPad,
          agentRegistry: agentRegistryPDA,
          agentWallet: agentWallet.publicKey,
          platformState: platformStatePDA,
        })
        .signers([agentWallet])
        .rpc();

      const rugScore = await program.account.rugScore.fetch(perfectRugScore);
      
      // Score = (100 * 0.4) + (100 * 0.3) + 20 + 10 = 40 + 30 + 20 + 10 = 100
      assert.equal(rugScore.score, 100);
      console.log("Perfect score achieved:", rugScore.score);
    });
  });
});
